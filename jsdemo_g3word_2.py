import requests, execjs, json, time, os
from jsonpath import jsonpath
from webjs.word3.f2.tools import download_img, headers, cookies
from webjs.word3.f2.loadmodel import gt3word


session = requests.Session()

### 1. 获取challenge 和 gt
def get_challengeid():
    params = {
        'source': 'main-fe-header',
        't': '0.7758525919151655',
    }
    url1  = 'https://passport.bilibili.com/x/passport-login/captcha'
    response = session.get(url1, params=params, cookies=cookies, headers=headers)
    resjson = response.json()
    challenge = jsonpath(resjson, '$..challenge')[0]
    gt = jsonpath(resjson, '$..gt')[0]
    return challenge, gt

### 2. 获取点击类型
def get_click_type(gt, challenge):
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        'callback': f'geetest_{int(time.time() * 1000)}'
    }
    ## 获取点击类型
    response = session.get(
        'https://api.geetest.com/ajax.php', headers=headers, params=params
    )
    restext = response.text
    result = json.loads(restext[restext.find("(") + 1:restext.rfind(")")])
    click_type = jsonpath(result, '$..result')[0]
    assert click_type == 'click', "点击类型不是 click"
    return click_type

### 3. 获取 json 详细信息
def get_gtresponse(gt, challenge):
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
        'callback': f'geetest_{int(time.time() * 1000)}',
    }
    response = session.get('https://api.geetest.com/get.php', params=params, headers=headers)
    restext = response.text
    result = json.loads(restext[restext.find("(") + 1:restext.rfind(")")])
    myc = jsonpath(result, '$..c')[0]
    mys = jsonpath(result, '$..s')[0]
    pic = jsonpath(result, '$..pic')[0]
    return myc, mys, pic


### 4. 最后验证
def validate(gt, challenge, w):
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        "w": w,
        'callback': f'geetest_{int(time.time() * 1000)}',
    }

    response = session.get('https://api.geetest.com/ajax.php',  headers=headers, params=params)
    return response.text



if __name__ == "__main__":

    ### 1. 获取challenge 和 gt
    challenge, gt = get_challengeid()

    ### 2. 获取点击类型
    click_type = get_click_type(gt, challenge)

    ### 3. 获取 json 详细信息
    myc, mys, pic = get_gtresponse(gt, challenge)
    time.sleep(1)
    ### 4. 下载图片,获取坐标, 并转为极验需要的格式
    os.makedirs('temp', exist_ok=True)
    download_img(pic, 'temp/a.jpg')
    out = gt3word.run('temp/a.jpg')
    # xyxy = poses2geetest(out.targets_xyxy)

    ### 5. 处理 w 参数
    time.sleep(1)
    import execjs
    with open("./webjs/word3/f2/biblg3word.js", 'r', encoding='utf-8') as f:
        jscode = f.read()
    ctx = execjs.compile(jscode)

    w = ctx.call('get_w', out.targets_xyxy,  pic,  gt, challenge, myc, mys )

    ### 6. 最后验证
    res = validate(gt, challenge, w)
    print(res)




