""" 
函数通用接口
"""
import base64
import hashlib
from typing import Optional, Union
import requests
from app.loadmodel import gt4icon, gt3nine, gt3word
from app.common import Input
from src.utils.utils import open_image
from fastapi import Request
from app.gt3.nine.ninejs import get_resjson, get_verify

token_list = ["abc", "abc1", "abcdQwm123dnine4", "abcdQwm123gtword3"] # abcdQwm123dnine4 这个 已出售给了客户, 请勿删除

def token_validation(input: Input, request: Request):
    # 请求对象,用来获取请求头,请求体等信息):
    ############################################################
    ###### 用于 js逆向, 这里用不到, 可以删除 ################
    ua = request.headers.get("user-agent", "")
    origin = request.headers.get("origin", "")
    referer = request.headers.get("referer", "")
    headers = {
        "user-agent": ua,
        "origin": origin,
        "referer": referer
    }
    ############################################################
    ############################################################
    ####################  简单的 token 验证  #######################
    input_data = input.model_dump()
    token = input_data.get("token", "")
    key = input_data.get("key", "")

    if token not in token_list and key not in token_list:
        return None, None
    
    input_data.pop("token", None)
    input_data.pop("key", None)

    return headers, input_data
    ############################################################



def set_imageSource(data: dict, headers = None) -> Optional[bytes]:
    """
    把传入的图片数据保存到本地，并返回图片的二进制数据
    :param data: 传入的图片数据,是一个字典
    如果 dataType 为 1, 则 imageSource 是一个 url, 则直接下载图片,保存图片(丢弃)
    如果 dataType 为 2, 则 imageSource 是一个 base64 编码的字符串, 则解码后保存图片
    :return: 返回图片的二进制数据
    """
    if data.get('dataType', None) == 1:
        rep = requests.get(
            data['imageSource'],
            verify=False,
            headers=headers
        )
        imageSource = rep.content
        img = [imageSource]
        extraicon = None
    elif data.get('dataType', None) == 2:
        img = data.get('imageSource', None)
        extraicon = data.get('extraicon', None)
        assert img is not None, "imageSource is None"
        assert isinstance(img, list), "imageSource must be a list"
    else:
        assert False, "dataType is not 1 or 2"

    imageSource_list = [open_image(i, rmalpha=True) for i in img]
    extraicon_list = [open_image(i, rmalpha=True) for i in extraicon] if extraicon else None
    return imageSource_list, extraicon_list

maplist = {
    "gt4icon": gt4icon.run,
    "gt3nine": gt3nine.run,
    "gt3word": gt3word.run
}
def get_res(obj_name: str, input_dict: dict, headers: dict):
    imageID = input_dict.get("imageID", "")
    imageSource_list, extraicon_list = set_imageSource(input_dict, headers=headers)
    # 获取对象
    res = maplist.get(obj_name)(imageSource_list[0], extraicon_list) # 调用对象的 run 方法
    targets_xyxy = res.targets_xyxy
    data = {"imageID": imageID, "res": targets_xyxy}
    return data




