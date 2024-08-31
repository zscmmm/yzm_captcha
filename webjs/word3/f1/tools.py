import base64
import requests
from urllib.parse import urljoin
from urllib import request
from typing import Union 
import os

def send_image2server(image_path: Union[str, bytes],
                      image_id: str = "string", 
                      server_url: str = "http://127.0.0.1:9100/gt3/word3"):
    """
    根据图片路径,读取图片,并发送到服务器, 获取返回结果,返回结果为json格式
    :param image_path: 图片路径, 
        str类型, 表示图片的路径,
        bytes类型, 表示图片的二进制数据,即图片的内容,一般是通过open('rb')读取的或者直接 request.get(url).content
    :param image_id: 图片id
    :param server_url: 服务器地址
    :return: 返回结果, json格式,里面包含识别的详细信息
    """
    if isinstance(image_path, bytes):
        image_data = image_path
    elif isinstance(image_path, str) and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
    else:
        raise ValueError("image_path should be bytes or str")
    data = {
        "dataType": 2,
        "imageSource": [base64.b64encode(image_data).decode('utf-8')],
        "imageID": image_id,
        "extraicon": None,
        "imageID": "string",
        "token": "abc1"
    }
    response = requests.post(server_url, json=data)
    try:
        resp_json = response.json()
        return resp_json['data']['res']
    except:
        return response.text
    

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





if __name__ == "__main__":
    import os
    image_path = os.path.join("docs", "a01.jpg")
    response = send_image2server(image_path)
    print(response.text)
    # import hashlib
    # import base64
    # with open(image_path, 'rb') as f:
    #     image_data = f.read()
    # imageSource =  base64.b64encode(image_data).decode('utf-8')
    # imageSource2 = base64.b64decode(bytes(imageSource, 'utf-8'))
    # hash_value = hashlib.md5(imageSource2).hexdigest()
    # print("Image Hash (MD5):", hash_value)


    




