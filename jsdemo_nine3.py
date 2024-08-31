import re, requests, time, uuid, execjs, json
from lxml import etree
from urllib.parse import urljoin
from jsonpath import jsonpath
from pathlib import Path
from webjs.nine3.utils import *
from webjs.word3.f2.loadmodel import gt3nine




headers = {
    'authority': 'gt4.geetest.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_captchaId():
    global headers
    session = requests.Session()    
    response = session.get('https://gt4.geetest.com/', headers=headers)

    HTML = etree.HTML(response.text)
    js_url = HTML.xpath('//script[contains(@src, "/assets/index")]/@src')[0]

    res = session.get(urljoin("https://gt4.geetest.com", js_url), headers=headers).text
    captchaId = re.search('captcha_id:"([0-9a-z]+)"', res).group(1)
    return captchaId, session




def get_resjson(captcha_id):
    params = {
        'callback': f'geetest_{int(time.time() * 1000)}',
        'captcha_id': captcha_id,
        'challenge': str(uuid.uuid4()),
        'client_type': 'web',
        'risk_type': 'nine',
        'lang': 'zh',
    }
    response = session.get('https://gcaptcha4.geetest.com/load', params=params, headers=headers)
    res = response.text
    resp_json = json.loads(res[res.find("(") + 1:res.rfind(")")])
    captcha_type =jsonpath(resp_json, '$..captcha_type')[0]
    assert captcha_type == 'nine', "captcha_type should be nine"

    kk, ss = 1, 1
    imgs_dir = ques_dir = "temp"
    Path(imgs_dir).mkdir(parents=True, exist_ok=True)
    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)

    ques, ques_count = generate_url(jsonpath(resp_json, '$..ques')[0])
    ques_path = generate_paths(ques_dir, f"ques_{kk}_{ss}", ques_count)
    download_img(ques, ques_path)
    return resp_json, captcha_id, imgs_path, ques_path



if __name__ == "__main__":
    ## 九宫格
    captcha_id, session = get_captchaId()

    resp_json, captcha_id, imgs_path, ques_path = get_resjson(captcha_id)


    time.sleep(1)
    out = gt3nine.run(imgs_path[0], ques_path)
    userresponse = out.nine_rowcol  # 九宫格的坐标

    #下面传递的参数都是从resp_json中获取的
    lot_number = jsonpath(resp_json, '$..lot_number')[0]
    nine_nums = jsonpath(resp_json, '$..nine_nums')[0]
    payload = jsonpath(resp_json, '$..payload')[0]
    payload_protocol = jsonpath(resp_json, '$..payload_protocol')[0]
    datetime = jsonpath(resp_json, '$..datetime')[0]
    process_token = jsonpath(resp_json, '$..process_token')[0]
    with open("webjs/nine3/demo.js", "r") as f:
        jscode = f.read()
    ctx = execjs.compile(jscode)
    w = ctx.call("get_w", captcha_id, lot_number, datetime, userresponse)

    params = {
        'callback': f'geetest_{int(time.time() * 1000)}',
        'captcha_id': captcha_id,
        'client_type': 'web',
        'lot_number': lot_number,
        'risk_type': 'nine',
        'payload': payload,
        'process_token': process_token,
        'payload_protocol': '1',
        'pt': '1',
        'w': w,
    }
    url3 = 'https://gcaptcha4.geetest.com/verify'
    response = requests.get(url3, params=params, headers=headers)

    print(response.text)