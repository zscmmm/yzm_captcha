import json, re, time, execjs, os, random, requests
from typing import Literal, Union
from webjs.word3.f1.tools import send_image2server, download_img


URL = [
    'https://passport.bilibili.com/x/passport-login/captcha',  # 初始化获取挑战
    'https://api.geetest.com/gettype.php',  # 初始化相关
    'https://api.geetest.com/ajax.php',  # 初始化相关
    'https://api.geetest.com/get.php',  # 获取图片
]

Method = Literal['get', 'post', 'POST', 'GET']
pattern = re.compile(r'\((.*?)\)', re.S)


class Gessts:
    # 设置请求session
    session = requests.Session()
    # 返回指定数据类型
    dataProcessors = {
        'json': lambda resp: resp.json(),
        'text': lambda resp: resp.text,
        'contents': lambda resp: resp.content
    }
    # 请求方式
    methodProcessors = {
        'get': session.get,
        'post': session.post
    }

    def __init__(self):
        self.cookies = None

        self.headers = {
            'authority': 'passport.bilibili.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.bilibili.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

    def ajax_requests(
            self, url: str, method: Method, headers: dict,
            cookies: dict, params: Union[dict, str, None],
            jsonData: Union[dict, None], retryTimes: int = 5,
            timeOut: int = 20
    ) -> requests.Response:
        # 初始化请求发送器以及数据获取器

        methodProcessor = self.methodProcessors[method]
        for _ in range(retryTimes):
            try:
                return methodProcessor(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    params=params,
                    data=json.dumps(jsonData, ensure_ascii=False, separators=(',', ':')),
                    timeout=timeOut
                )
            except Exception as e:
                print(
                    f"错误链接: {url}",
                    f"请求出现错误, 正在重试: {_}/{retryTimes}",
                    f"错误信息为: {e}",
                    sep='\n'
                )
        else:
            raise '重试5次后仍然无法获取数据，可能是加密参数错误或者ip风控'

    def init_challenge(self):
        """
        通过 B 站的接口获取验证码的 challenge 和 gt
        """
        url = URL[0]
        params = {
            'source': 'main-fe-header',
            't': '0.26599063907171017',
        }
        resp: dict = self.ajax_requests(
            url=url,
            params=params,
            method='get',
            jsonData=None,
            cookies=self.cookies,
            headers=self.headers
        ).json()
        challenge, gt = resp['data']['geetest'].values()
        return challenge, gt

    def get_all_info(self, challenge: str, gt: str, header:dict = None, cookies:dict = None) -> tuple:
        """
        根据 gt 和 challenge 获取 c, s 以及图片的地址等详细参数
        这个函数是获取c，s以及坐标信息，这里的坐标是未经过处理的
        参数:
            gt: str: 
            challenge: str: 
            header: dict: 请求头, 建议越全面越好, 比如: 
                {
                    'authority': ***,
                    'accept':  ***,
                    'accept-language':  ***,
                    'Referer': ***,
                    'user-agent': ***,
                }
            cookies: dict: cookies ,这两个参数传递给get_all_info, 不过一般情况下 cookies 不需要传递
        返回:
            tuple: 返回图片的地址(带前缀), gt, challenge, c, s
        """
        if header is not None and isinstance(header, dict):
            hd = header
        else:
            hd = self.headers
        if cookies is not None and isinstance(cookies, dict):
            ck = cookies
        else:
            ck = self.cookies
        # ck = None   # 这里不需要cookies, 但是为了方便调试，先注释掉
        now_stamp = int(time.time() * 1000)
        self._now_stamp = now_stamp
        par = {
            'gt': gt,
            'callback': f'geetest_{self._now_stamp}',
        }
        self.ajax_requests(url=URL[1], headers=hd, cookies=ck, jsonData=None, method='get', params=par)
        par.update({
            'challenge': challenge,
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
            'w': '',
        })
        self.ajax_requests(url=URL[3], method='get', headers=hd, cookies=ck, params=par, jsonData=None)
        self.ajax_requests(url=URL[2], method='get', headers=hd, cookies=ck, params=par, jsonData=None)
        par.update({
            'is_next': 'true',
            'type': 'click',
            'https': 'false',
            'protocol': 'https://',
            'offline': 'false',
            'product': 'embed',
            'api_server': 'api.geetest.com',
            'isPC': 'true',
            'autoReset': 'true',
            'width': '100%',
            'callback': f'geetest_{self._now_stamp}',
        })
        resp = self.ajax_requests(url=URL[3], method='get', headers=hd, cookies=ck,  params=par, jsonData=None) 
        # 上述顺序不能打乱，必须严格相同
        result: dict = json.loads(pattern.findall(resp.text)[0])['data']
        pic: str = 'https://static.geetest.com' + result['pic']
        c = result['c']
        s = result['s']
        assert "word" in pic, "这不是点选验证码"
        return pic, gt, challenge, c, s
    
    def xyxy2gt(self, xyxy_list: list[list[float]] ) -> str:
        """
        将坐标转换为极验需要的格式
        """
        assert isinstance(xyxy_list, list), "xyxy_list 应该是一个列表"
        assert all(len(i) == 4 for i in xyxy_list), "xyxy_list 中的每个元素应该是一个长度为4的列表"
        new = []
        # 处理坐标，变为极验需要的样子
        for code in xyxy_list:
            x, y = (code[0] + code[2]) / 2, (code[1] + code[3]) / 2
            final_x = int(round(int(x) / 333.375 * 100 * 100, 0))
            final_y = int(round(int(y) / 333.375 * 100 * 100, 0))
            final = f'{final_x}_{final_y}'
            new.append(final)

        return ','.join(new)

    def do_verify(self, challenge: str, gt: str, pic_name:str="image.jpg", header:dict = None, cookies:dict = None) -> dict:
        """
        处理验证的主要函数
        参数:
            gt: str: 
            challenge: str:
            pic_name: str: 图片的保存路径,本地路径, 默认为 image.jpg
            header: dict: 请求头, 建议越全面越好, 比如: 
                {
                    'authority': ***,
                    'accept':  ***,
                    'accept-language':  ***,
                    'Referer': ***,
                    'user-agent': ***,
                }
            cookies: dict: cookies ,这两个参数传递给get_all_info, 不过一般情况下 cookies 不需要传递
        返回:
            dict: 返回验证的结果
        """
        pic, gt, challenge, c, s = self.get_all_info(challenge, gt, header, cookies)
        # 获取坐标信息
        download_img(pic, pic_name)
        codes = send_image2server(pic_name)
        print(f"处理之前的坐标: {codes}")
        stringCodes = self.xyxy2gt(codes)
        print(
            f'处理后坐标: {stringCodes}',
            f'图片地址: {pic}',
            f'gt:{gt}, challenge:{challenge}',
            f'c: {c}, s: {s}', sep='\n'
        )
        with open('./webjs/word3/f1/demo.js', 'r', encoding='utf-8') as f:
            jscode = f.read()
        ctx = execjs.compile(jscode)
        print(f"stringCodes: {stringCodes}")
        w = ctx.call('get_w', stringCodes, pic, gt, challenge, c, s )

        ### 方法 2
        # with open('./webjs/word3/f2/biblg3word.js', 'r', encoding='utf-8') as f:
        #     jscode = f.read()
        # ctx = execjs.compile(jscode)
        # w = ctx.call('get_w', stringCodes, pic, gt, challenge, c, s )

        params = {
            "gt": gt,
            "challenge": challenge,
            "lang": "zh-cn",
            "pt": "0",
            "client_type": "web",
            "w": w,
            "callback": f"geetest_{self._now_stamp}",
        }
        # print(f"参数: {params}")
        # 避免出现点选过快的情况
        time.sleep(random.uniform(3, 6))
        resp = self.ajax_requests(
            url='https://api.geetest.com/ajax.php',
            method='get',
            headers=self.headers,
            cookies=self.cookies,
            jsonData=None,
            params=params
        )
        # 处理 jsonp 数据
        try:
            resp_json = resp.json()
        except:
            resp_json = self.headle_jsonp(resp.text)
        return resp_json
        
    def is_valid_jsonp(self, text: str) -> bool:
        """
        判断是否是 JSONP 格式的数据,以 'geetest_数字(' 开头. 当然可以换成其他的, 比如: re.compile(r'\((.*?)\)', re.S)
        参数:
            text: str: 需要判断的文本
        返回:
            bool: 返回是否是 JSONP 格式的数据
        """
        if not isinstance(text, str):
            return False
        pattern = re.compile(r"^geetest_\d+\(") # 
        match = pattern.match(text)
        # 如果匹配成功，返回 True，否则返回 False
        return bool(match)
    def headle_jsonp(self, text) -> dict:
        """
        处理 JSONP 格式的数据,去掉头尾的无用字符
        参数:
            text: str: 需要处理的文本
        返回:
            dict: 返回处理后的数据,如果不是 JSONP 格式的数据,则抛出异常
        """

        if self.is_valid_jsonp(text):
            jsonppattern = re.compile(r'\((.*?)\)', re.S)
            return json.loads(jsonppattern.findall(text)[0])
        else:
            assert False, '不是 JSONP 格式的数据'


if __name__ == '__main__':
    bili = Gessts()
    challenge, gt = bili.init_challenge() # 调用 b 站的接口获取 challenge 和 gt
    print(f"challenge: {challenge}, gt: {gt}")
    pic_name = os.path.join("temp", f"pic_{challenge[0:5]}.jpg")
    os.makedirs(os.path.dirname(pic_name), exist_ok=True)
    resp = bili.do_verify(challenge, gt, pic_name) #传递参数获取验证结果
    print(resp)