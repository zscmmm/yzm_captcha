from urllib.parse import urljoin
from urllib import request
from typing import Union 
import os

def download_img(url: Union[str, list], path: Union[str, list]) -> None:
    """
    通过url下载图片,已经被 urllib.request 封装好了的
    :param url: 图片url
    :param path: 保存路径,带后缀名
    """
    if isinstance(url, str) and isinstance(path, str):
        if r'https://static.geetest.com' in url:
            pass
        else:
            url = urljoin('https://static.geetest.com', url)
        if r"/" in path or r"\\" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        request.urlretrieve(url, path)

    elif isinstance(url, list) and isinstance(path, list):
        assert len(url) == len(path), "url和path长度不一致"
        if r"/" in path or r"\\" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        
        for i in range(len(url)):
            if r'https://static.geetest.com' in url[i]:
                pass
            else:
                url[i] = urljoin('https://static.geetest.com', url[i])
            request.urlretrieve(url[i], path[i])



def poses2geetest(poses: list) -> str:
    """
    处理坐标，变为极验需要的样子
    参数:
        poses: list: 坐标信息, 格式是: [[x1, y1, x2, y2], [x1, y1, x2, y2], ...] 需要转为极验需要的格式
    返回:
        str: 返回处理后的坐标
    """
    new = []
    for pose in poses:
        x, y = (pose[0] + pose[2]) / 2, (pose[1] + pose[3]) / 2
        final_x = int(round(int(x) / 333.375 * 100 * 100, 0))
        final_y = int(round(int(y) / 333.375 * 100 * 100, 0))
        final = f'{final_x}_{final_y}'
        new.append(final)
    stringCodes = ','.join(new)
    return stringCodes


cookies = None

headers = {
    'authority': 'passport.bilibili.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'referer': 'https://www.bilibili.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}

HD= headers.copy()
