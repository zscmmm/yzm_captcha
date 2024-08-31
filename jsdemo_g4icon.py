import requests, json, time, execjs, uuid, os
from jsonpath import jsonpath
from webjs.word3.f2.loadmodel import gt4icon
from webjs.icon4.tools import xyxy2gtformat, download_img, headers, cookies, now_str
"""
由于该网站比较严格,需要 header 和 cookies, 以及一些参数, 本代码只是一个示例, 不能直接运行
"""
params = {
    'scene_type': '1',
    'now': now_str,
    'reason': 'user.mihoyo.com#/login/password',
    'action_type': 'login_by_password',
    'account': '19196951600',
    't': now_str,
}


session = requests.session()
for ii in range(10):
    try:
        url1 = 'https://webapi.account.mihoyo.com/Api/create_mmt'
        response = session.get(url1, params=params, cookies=cookies, headers=headers)
        gt1 = jsonpath(response.json(), '$..gt')
        mmt_key = jsonpath(response.json(), '$..mmt_key')
        if gt1:
            gt = gt1[0]
            break   
        time.sleep(1)
        data = {
            'account': '19194931000',
            'password': 'MERS6bUrEYw9LMhf2mLL9j2CeWmdowp5Vgadu58jZeYN7LT1BdWIh8ASiD35xaFRoPKg3Uz5B4ka4P+QzQB6ViopvqRPUW3VOhcpZLM/RM8RIDvHOtRZzHwJjGyQfw/gbZf2YPbARE3kplpvbTYvcX/3SjSuLkqG0XJapIvfKFc=',
            'is_crypto': 'true',
            'mmt_key': mmt_key,
            'source': 'user.mihoyo.com',
            't': str(int(time.time() * 1000)),
        }
        url2 = 'https://webapi.account.mihoyo.com/Api/login_by_password'
        response = session.post(url2, cookies=cookies, headers=headers, data=data)
        time.sleep(1)
        gt2 = jsonpath(response.json(), '$..gt')
        if gt2:
            gt = gt2[0]
            break
    except:
        print(f"第{ii}次获取gt和mmt_key失败")
        continue    


params = {
    'callback': f'geetest_{int(time.time() * 1000)}',
    'captcha_id': gt,
    'challenge': str(uuid.uuid4()),
    'client_type': 'web',
    'risk_type': 'icon',
    'user_info': json.dumps({"mmt_key": mmt_key }, separators=(',', ':')),
    'lang': 'zho',
}


response = session.get('https://gcaptcha4.geetest.com/load', params=params, cookies=cookies, headers=headers)
res = response.text
json_data = json.loads(res[res.index("(") + 1:res.rindex(")")])
os.makedirs("temp", exist_ok=True)

# with open("temp/icon4.json", "w") as f:
#     json.dump(json_data, f, ensure_ascii=False, indent=2)

imgs = jsonpath(json_data, '$..imgs')[0]
download_img(imgs, "temp/a.png")

ques = jsonpath(json_data, '$..ques')[0]
ques_path = [f"temp/ques_{i}.png" for i in range(len(ques))] 
download_img(ques, ques_path)

imgs_path = "temp/a.png"

out = gt4icon.run(imgs_path, ques_path)
xyxy = out.targets_xyxy

userresponse = xyxy2gtformat(xyxy)

with open("webjs/icon4/demo_g4icon.js", "r") as f:
    jscode = f.read()
ctx = execjs.compile(jscode)


lot_number = jsonpath(json_data, '$..lot_number')[0]
pow_detail = jsonpath(json_data, '$..pow_detail')[0]
detail_time = jsonpath(pow_detail, '$..datetime')[0]
payload = jsonpath(json_data, '$..payload')[0]
process_token = jsonpath(json_data, '$..process_token')[0]


w = ctx.call("get_w2", gt, lot_number, detail_time, userresponse)



params = {
    'callback': f'geetest_{int(time.time() * 1000)}',
    'captcha_id': gt,
    'client_type': 'web',
    'lot_number': lot_number,
    'risk_type': 'icon',
    'payload': payload,
    'process_token': process_token,
    'payload_protocol': '1',
    'pt': '1',
    'w': w,
}

response = session.get('https://gcaptcha4.geetest.com/verify', params=params, cookies=cookies, headers=headers)
print(response.text)    

