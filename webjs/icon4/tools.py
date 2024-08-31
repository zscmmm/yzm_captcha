from urllib import request
import os
from typing import Union
from urllib.parse import urljoin
import time
def download_img(url: Union[str, list], path: Union[str, list]) -> None:
    """
    通过url下载图片,已经被 urllib.request 封装好了的
    :param url: 图片url
    :param path: 保存路径,带后缀名
    """
    if isinstance(url, str) and isinstance(path, str):
        if r"/" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        if "https" not in url:
            url = urljoin("https://static.geetest.com", url)
        request.urlretrieve(url, path)

    elif isinstance(url, list) and isinstance(path, list):
        assert len(url) == len(path), "url和path长度不一致"
        for i in range(len(url)):
            if "https" not in url[i]:
                url[i] = urljoin("https://static.geetest.com", url[i])
            request.urlretrieve(url[i], path[i])

def xyxy2gtformat(xyxy):
    xyxy_center = []
    for point in xyxy:
        x = (point[0] + point[2]) // 2
        y = (point[1] + point[3]) // 2
        xyxy_center.append([x, y])

    new_points = []
    for point in xyxy_center:
        x = point[0] * 32   # 32 和 48 是手动计算出来的
        y = point[1] * 48
        new_points.append([x, y])
    return new_points




now_str = str(int(time.time() * 1000))

cookies = {
    'aliyungf_tc': '180a86da32644284df3bb8fbeeb91f03283c3444515b4888d1f04eb2eb504862',
    '_MHYUUID': 'b337f507-855b-4c73-afd8-13b573b69469',
    'DEVICEFP_SEED_ID': 'f42cee7a2fbc6a2b',
    'DEVICEFP_SEED_TIME': now_str,
    'DEVICEFP': '38d7f7f987b09'
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://user.mihoyo.com',
    'Pragma': 'no-cache',
    'Referer': 'https://user.mihoyo.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'x-rpc-client_type': '4',
    'x-rpc-device_fp': '38d7f7f987b09',
    'x-rpc-device_id': 'b337f507-855b-4c73-afd8-13b573b69469',
    'x-rpc-device_model': 'Microsoft%20Edge%20120.0.0.0',
    'x-rpc-device_name': 'Microsoft%20Edge',
    'x-rpc-mi_referrer': 'https://user.mihoyo.com/',
    'x-rpc-source': 'accountWebsite',
}
