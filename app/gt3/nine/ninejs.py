
"""
主要实现九宫格验证码的识别
"""
import re, requests, time, uuid, execjs, json
from jsonpath import jsonpath
from pathlib import Path
from webjs.word3.f2.loadmodel import gt3nine
from webjs.nine3.utils import *


headers = {
    'authority': 'gt4.geetest.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}  

def get_resjson(captcha_id, headers=None):
    if headers is None:
        headers = headers


    session = requests.Session() 
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
    imgs_dir = ques_dir = "temp_nine"
    Path(imgs_dir).mkdir(parents=True, exist_ok=True)
    imgs, imgs_count = generate_url(jsonpath(resp_json, '$..imgs')[0])
    imgs_path = generate_paths(imgs_dir, f"img_{kk}_{ss}", imgs_count)
    download_img(imgs, imgs_path)

    ques, ques_count = generate_url(jsonpath(resp_json, '$..ques')[0])
    ques_path = generate_paths(ques_dir, f"ques_{kk}_{ss}", ques_count)
    download_img(ques, ques_path)
    return resp_json, captcha_id, imgs_path, ques_path, session, headers


def get_verify(session, captcha_id, resp_json, userresponse, headers):
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
    response = session.get(url3, params=params, headers=headers)
    session.close()
    return response.text



def get_resjs(input_dict: dict, headers: dict,  
              get_resjson = get_resjson, get_verify = get_verify):
    '''
    四代九宫格js, 传入验证码id, 返回验证结果, 
    '''
    try:
        captcha_id = input_dict.get("gt", None)
        assert captcha_id is not None, "captcha_id is None"
    except:
        return {"code": 400, "msg": "captcha_id is None", "data": {}}
    if headers is None:
        headers = headers
        
    resp_json, captcha_id, imgs_path, ques_path, session, headers = get_resjson(captcha_id, headers)
    out = gt3nine.run(imgs_path[0], ques_path)
    userresponse = out.nine_rowcol  
    resp = get_verify(session, captcha_id, resp_json, userresponse, headers)
    try:
        resp1 = resp.json()  
    except:
        try:
            resp1 = json.loads(resp[resp.find("(") + 1:resp.rfind(")")])
        except:
            resp1 = resp.text
    if not resp1:
        return {"code": 500, "msg": "Server Error", "data": {}}
    return resp1

if __name__ == "__main__":
    pass