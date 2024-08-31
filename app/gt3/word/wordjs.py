
import requests, execjs, json, time, os
from jsonpath import jsonpath
from webjs.word3.f2.tools import download_img, headers, cookies, HD
from webjs.word3.f2.loadmodel import gt3word
import execjs
import random
from typing import Any
from loguru import logger
import asyncio
import uuid
### 2. 获取点击类型
def get_click_type(gt, challenge, headers=None):
    headers = headers if headers is not None else HD
    session = requests.Session()
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        'callback': f'geetest_{int(time.time() * 1000) - 1000}'
    }
    ## 获取点击类型

    response = session.get('https://api.geetest.com/ajax.php', headers=headers, params=params)
    restext = response.text
    result = json.loads(restext[restext.find("(") + 1:restext.rfind(")")])
    click_type = jsonpath(result, '$..result')[0]
    # assert click_type == 'click', "点击类型不是 click"
    if click_type != 'click':
        logger.warning("点击类型不是 click")
    return click_type, session, headers


### 3. 获取 json 详细信息
def get_gtresponse(gt, challenge, session,headers=None):
    headers = headers if headers is not None else HD
    params = {
        'is_next': 'true',
        'type': 'click',
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'https': 'false',
        'protocol': 'https://',
        'offline': 'false',
        'product': 'embed',
        'api_server': 'api.geetest.com',
        'isPC': 'true',
        'autoReset': 'true',
        'width': '100%',
        'callback': f'geetest_{int(time.time() * 1000) - 1000}',
    }
    response = session.get('https://api.geetest.com/get.php', params=params, headers=headers)
    restext = response.text
    result = json.loads(restext[restext.find("(") + 1:restext.rfind(")")])
    myc = jsonpath(result, '$..c')[0]
    mys = jsonpath(result, '$..s')[0]
    pic = jsonpath(result, '$..pic')[0]
    return myc, mys, pic, session, headers, result




def get_resjson(gt, challenge, session, headers=None):
    '''
    三代点选js, 传入验证码id, 返回验证结果, 
    '''
    headers = headers if headers is not None else HD
    ### 3. 获取 json 详细信息
    myc, mys, pic, session, headers, result = get_gtresponse(gt, challenge, session, headers)
    ### 4. 下载图片,获取坐标, 并转为极验需要的格式
    os.makedirs('temp', exist_ok=True)
    imgs_path = 'temp/a.jpg'
    download_img(pic, imgs_path)

    return myc, mys, pic, session, headers, result, imgs_path

  

### 4. 最后验证
def validate(gt, challenge, w, session,  headers: dict = None):
    headers = headers if headers is not None else HD
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        "w": w,
        'callback': f'geetest_{int(time.time() * 1000) + 1000}',
    }
    time.sleep(random.uniform(0.1, 0.3)) #### 休息一下,防止太快
    response = session.get('https://api.geetest.com/ajax.php',  headers=headers, params=params)
    session.close()
    return response.text




with open("./webjs/word3/f2/biblg3word.js", 'r', encoding='utf-8') as f:
    jscode = f.read()
ctx = execjs.compile(jscode)

def get_resjs(input_dict: dict, 
              headers: dict,  
              get_resjson = get_resjson, 
              validate = validate,
              ctx = ctx,
              gt3word = gt3word,
              get_click_type = get_click_type
    ) -> dict[str, Any] | Any:
    '''
    三代点选js, 传入验证码id, 返回验证结果, 
    '''
    try:
        gt = input_dict.get("gt", None)
        challenge = input_dict.get("challenge", None)
        assert gt is not None, "captcha_id is None"
        assert challenge is not None, "challenge is None"
    except:
        return {"code": 400, "msg": "captcha_id is None", "data": {}}

    headers = headers if headers is not None else HD
    ### 2. 获取点击类型
    click_type, session, headers = get_click_type(gt, challenge, headers)
    if click_type != 'click':
        return {"code": 400, "msg": "click_type is not click", "data": {}}
    ### 3. 获取 json 详细信息 --- 下载图片
    myc, mys, pic, session, headers, result, imgs_path = get_resjson(gt, challenge, session, headers)
    ### 4.获取坐标
    out = gt3word.run(imgs_path)
    xyxy = out.targets_xyxy
    time.sleep(random.uniform(0.9, 1.3)) #### 休息一下,防止太快
    ### 4. 获取 w--- 已经自动转换为极验需要的格式
    w = ctx.call('get_w',xyxy ,  pic,  gt, challenge, myc, mys )
    
    ### 5. 最后验证
    resptext = validate(gt, challenge, w, session, headers)
    try:
        resp1 = json.loads(resptext[resptext.find("(") + 1:resptext.rfind(")")])
    except:
        try:
            resp1 = json.loads(resptext)
        except:
            resp1 = resptext
    if not resp1:
        return {"code": 500, "msg": "Server Error", "data": {"w": w, "xyxy": xyxy, "pic": pic, "myc": myc, "mys": mys, "result": result}}
    return resp1



async def aioget_resjs(input_dict: dict, 
              headers: dict,  
              get_resjson = get_resjson, 
              validate = validate,
              ctx = ctx,
              gt3word = gt3word,
              get_click_type = get_click_type
    ) -> dict[str, Any] | Any:
    '''
    三代点选js, 传入验证码id, 返回验证结果, 
    '''
    try:
        gt = input_dict.get("gt", None)
        challenge = input_dict.get("challenge", None)
        assert gt is not None, "captcha_id is None"
        assert challenge is not None, "challenge is None"
    except:
        return {"code": 400, "msg": "captcha_id is None", "data": {}}

    headers = headers if headers is not None else HD
    ### 2. 获取点击类型
    click_type, session, headers = get_click_type(gt, challenge, headers)
    if click_type != 'click':
        return {"code": 400, "msg": "click_type is not click", "data": {}}
    ### 3. 获取 json 详细信息 --- 下载图片
    myc, mys, pic, session, headers, result, imgs_path = get_resjson(gt, challenge, session, headers)
    ### 4.获取坐标
    out = gt3word.run(imgs_path)
    xyxy = out.targets_xyxy
    # time.sleep(random.uniform(0.9, 1.3)) #### 休息一下,防止太快
    tt = random.uniform(1, 1.5)
    # 产生一个 uuid
    random_uuid =  str(uuid.uuid4())
    logger.warning(f"uuid: {random_uuid}, 休息时间: {tt}")
    await asyncio.sleep(tt)
    logger.warning(f"uuid: {random_uuid}, 休息结束")
    ### 4. 获取 w--- 已经自动转换为极验需要的格式
    w = ctx.call('get_w',xyxy ,  pic,  gt, challenge, myc, mys )
    
    ### 5. 最后验证
    resptext = validate(gt, challenge, w, session, headers)
    try:
        resp1 = json.loads(resptext[resptext.find("(") + 1:resptext.rfind(")")])
    except:
        try:
            resp1 = json.loads(resptext)
        except:
            resp1 = resptext
    if not resp1:
        return {"code": 500, "msg": "Server Error", "data": {"w": w, "xyxy": xyxy, "pic": pic, "myc": myc, "mys": mys, "result": result}}
    return resp1


if __name__ == "__main__":
    pass