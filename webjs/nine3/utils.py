
import json
import os
import random

from urllib import request
from typing import Union 
from urllib.parse import urljoin
from lxml import etree
from jsonpath import jsonpath
import copy

def create_directory(directory):
    os.makedirs(directory, exist_ok=True)

def write_json_file(json_data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, sort_keys=True)

def generate_filename_prefix(ii):
    ss = random.randint(10000, 99999)
    kk = str(ii).zfill(5)
    return kk, ss

def generate_paths(directory, prefix, count):
    if count == 1:
        return [os.path.join(directory, f"{prefix}.png")]
    else:
        return [os.path.join(directory, f"{prefix}_{i}.png") for i in range(count)]
    
   


def download_img(url: Union[str, list], path: Union[str, list]) -> None:
    """
    通过url下载图片,已经被 urllib.request 封装好了的
    :param url: 图片url
    :param path: 保存路径,带后缀名
    """
    if isinstance(url, str) and isinstance(path, str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        request.urlretrieve(url, path)

    elif isinstance(url, list) and isinstance(path, list):
        assert len(url) == len(path), "url和path长度不一致"
        for i in range(len(url)):
            request.urlretrieve(url[i], path[i])

def handle_json_data(resp_json: dict):
    try:
        data = copy.deepcopy(resp_json['data'])
        if isinstance(data, str):
            data = json.loads(data)
            resp_json['data'] = data
        return resp_json
    except:
        return resp_json

def generate_list(i:str|list) -> list:
    if isinstance(i, str):
        return [i]
    else:
        return i
def generate_url(imgs: str|list) -> Union[list, int]:
    imgs = generate_list(imgs)
    imgs_list = [urljoin("https://static.geetest.com/", img) for img in imgs]
    return imgs_list, len(imgs_list)


def from_json_download_imgs_icon(resp_json: dict, ii: int):
    resp_json = handle_json_data(resp_json)
    json_dir = "icon4_json"
    imgs_dir = "icon4_imgs"
    ques_dir = "icon4_ques"

    create_directory(json_dir)
    create_directory(imgs_dir)
    create_directory(ques_dir)

    kk, ss = generate_filename_prefix(ii)
    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json")
    write_json_file(resp_json, filejson)

    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)

    ques, ques_count= generate_url(jsonpath(resp_json, '$..ques')[0])
    ques_path = generate_paths(ques_dir, f"ques_{kk}_{ss}", ques_count)
    download_img(ques, ques_path)
    return ii



def from_json_download_imgs_silde(resp_json: dict, ii: int):
    resp_json = handle_json_data(resp_json)
    json_dir = "slide4_json"
    slide_dir = "slide4_slide"
    bg_dir = "slide4_bg"

    create_directory(json_dir)
    create_directory(slide_dir)
    create_directory(bg_dir)

    kk, ss = generate_filename_prefix(ii)

    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json")
    write_json_file(resp_json, filejson)

    m_slice, m_slice_count = generate_url(jsonpath(resp_json, '$..slice')[0])
    m_slice_path = generate_paths(slide_dir, f"slice_{kk}_{ss}", m_slice_count)
    download_img(m_slice, m_slice_path)

    m_bg, m_bg_count = generate_url(jsonpath(resp_json, '$..bg')[0])
    m_bg_path = generate_paths(bg_dir, f"bg_{kk}_{ss}", m_bg_count)
    download_img(m_bg, m_bg_path)

    return ii





def from_json_download_imgs_phrase(resp_json: dict, ii: int):
    resp_json = handle_json_data(resp_json)
    json_dir = "phrase4_json"
    imgs_dir = "phrase4_imgs"

    create_directory(json_dir)
    create_directory(imgs_dir)

    kk, ss = generate_filename_prefix(ii)
    
    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json")
    write_json_file(resp_json, filejson)

    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)
    return ii



def from_json_download_imgs_winlinze(resp_json: dict, ii: int):
    resp_json = handle_json_data(resp_json)
    json_dir = "winlinze4_json"
    imgs_dir = "winlinze4_imgs"

    create_directory(json_dir)
    create_directory(imgs_dir)

    kk, ss = generate_filename_prefix(ii)
    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json")
    write_json_file(resp_json, filejson)

    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)
    return ii


def from_json_download_imgs_nine(resp_json: dict, ii: int):
    resp_json = handle_json_data(resp_json)
    json_dir = "nine4_json"
    imgs_dir = "nine4_imgs"
    ques_dir = "nine4_ques"
    create_directory(json_dir)
    create_directory(imgs_dir)
    create_directory(ques_dir)

    kk, ss = generate_filename_prefix(ii)
    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json")
    write_json_file(resp_json, filejson)

    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)

    ques, ques_count = generate_url(jsonpath(resp_json, '$..ques')[0])
    ques_path = generate_paths(ques_dir, f"ques_{kk}_{ss}", ques_count)
    download_img(ques, ques_path)
    return ii




def process_and_download(
        resp_json: dict,  #返回的json
        ii: int,  #计数
        imgtype: str,  #类型
        imgs_key: str = 'imgs', #图片的key
        additional_key: str = None, #额外的图片保存目录路径
    ) -> int:
    resp_json = handle_json_data(resp_json)
    json_dir = f"{imgtype}_json"
    imgs_dir = f"{imgtype}_{imgs_key}"
    create_directory(json_dir)
    create_directory(imgs_dir)

    imgs_file_prefix = imgs_key #以imgs_key为前缀
    
    kk, ss = generate_filename_prefix(ii)
    filejson = os.path.join(json_dir, f"res_{kk}_{ss}.json") #写入json文件
    write_json_file(resp_json, filejson)

    imgs_url, imgs_count = generate_url(jsonpath(resp_json, f'$..{imgs_key}')[0])
    imgs_path = generate_paths(imgs_dir, f"{imgs_file_prefix}_{kk}_{ss}", imgs_count)
    download_img(imgs_url, imgs_path)

    if additional_key:
        additional_dir = f"{imgtype}_{additional_key}"
        additional_file_prefix = additional_key #以additional_key为前缀
        create_directory(additional_dir)
        additional_url, additional_count = generate_url(jsonpath(resp_json, f'$..{additional_key}')[0])
        additional_path = generate_paths(additional_dir, f"{additional_file_prefix}_{kk}_{ss}", additional_count)
        download_img(additional_url, additional_path)
    return ii

# ##### 一个统一的函数
# process_and_download(resp_json, ii, "icon4", "imgs", "ques")
# process_and_download(resp_json, ii, "slide4", "slice", "bg")
# process_and_download(resp_json, ii, "phrase4", "imgs")
# process_and_download(resp_json, ii, "winlinze4", "imgs")
# process_and_download(resp_json, ii, "nine4", "imgs", "ques")
