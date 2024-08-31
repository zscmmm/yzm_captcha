const NodeRSA = require('node-rsa');
const crypto = require('crypto');
const CryptoJS = require("crypto-js");
function get_key() {
    var s4 = "";
    for (i = 0; i < 4; i++) {
        s4 = s4 + ((1 + Math["random"]()) * 65536 | 0)["toString"](16)["substring"](1);
    }
    return s4;
}
function MD5_Encrypt(word) {
    return CryptoJS.MD5(word).toString();
}
function AES_Encrypt(key, word) {
    var srcs = CryptoJS.enc.Utf8.parse(word);
    var encrypted = CryptoJS.AES.encrypt(srcs, CryptoJS.enc.Utf8.parse(key), {
        iv: CryptoJS.enc.Utf8.parse("0000000000000000"),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return CryptoJS.enc.Hex.stringify(CryptoJS.enc.Base64.parse(encrypted.toString()));
}
function RSA_encrypt(data) {
    const public_key_1 = '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81';
    const public_key_2 = '10001';
    const public_key = new NodeRSA();
    public_key.importKey({
        n: Buffer.from(public_key_1, 'hex'),
        e: parseInt(public_key_2, 16),
    }, 'components-public');
    const encrypted = crypto.publicEncrypt({
        key: public_key.exportKey('public'),
        padding: crypto.constants.RSA_PKCS1_PADDING
    }, Buffer.from(data));
    return encrypted.toString('hex');
}




function sha256(str) {
  const hash = crypto.createHash('sha256');
  hash.update(str);
  return hash.digest('hex');
}

function get_w2(gt, lot_number, detail_time, userresponse){
  let randomkey = get_key()

  passtime = 3000 + Math.floor(Math.random() * 1000)
  pow_msg = '1' + "|" + 12 + "|" + 'sha256' + "|" + detail_time + "|" + gt + "|" + lot_number + "|" + '' + "|" + randomkey
  pow_sign = sha256(pow_msg)
    // 输入的坐标格式: 
    // userresponse = [[1554,6199],[1819,2771],[4569,3665]]
  xiyu = {
    "passtime": passtime,
    "userresponse": userresponse, 
    "device_id": "70ad34ab80cef354efa5b79c622d5ad3",
    "lot_number": lot_number,
    "pow_msg": pow_msg,
    "pow_sign": pow_sign,
    "geetest": "captcha",
    "lang": "zh",
    "ep": "123",
    "biht": "1426265548",
    "gee_guard": {
        "env": {
            "sf": {
                "data": [
                    "Arial Unicode MS",
                    "Gill Sans",
                    "Helvetica Neue",
                    "Menlo"
                ]
            },
            "seaof": {
                "data": {
                    "tdf": 148.859375,
                    "elp": 148.859375,
                    "fos": 144.3125,
                    "pos": 148.859375,
                    "onm": 133.0625,
                    "nmi": 9.3125,
                    "mys": 146.09375
                }
            },
            "aosua": {
                "data": 124.04344968475198
            },
            "ecs": {
                "data": [
                    30,
                    0,
                    0,
                    0
                ]
            },
            "uscpo": {},
            "sal": {
                "data": [
                    [
                        "zh-CN"
                    ]
                ]
            },
            "hoc": {
                "data": 30
            },
            "ydmed": {
                "data": 8
            },
            "ncs": {
                "data": [
                    900,
                    1440
                ]
            },
            "yah": {
                "data": 8
            },
            "eit": {
                "data": "Asia/Shanghai"
            },
            "ees": {
                "data": true
            },
            "els": {
                "data": true
            },
            "bni": {
                "data": true
            },
            "epo": {
                "data": false
            },
            "sdspc": {},
            "mlp": {
                "data": "MacIntel"
            },
            "slp": {
                "data": [
                    {
                        "name": "PDF Viewer",
                        "description": "Portable Document Format",
                        "mimeTypes": [
                            {
                                "type": "application/pdf",
                                "suffixes": "pdf"
                            },
                            {
                                "type": "text/pdf",
                                "suffixes": "pdf"
                            }
                        ]
                    },
                    {
                        "name": "Chrome PDF Viewer",
                        "description": "Portable Document Format",
                        "mimeTypes": [
                            {
                                "type": "application/pdf",
                                "suffixes": "pdf"
                            },
                            {
                                "type": "text/pdf",
                                "suffixes": "pdf"
                            }
                        ]
                    },
                    {
                        "name": "Chromium PDF Viewer",
                        "description": "Portable Document Format",
                        "mimeTypes": [
                            {
                                "type": "application/pdf",
                                "suffixes": "pdf"
                            },
                            {
                                "type": "text/pdf",
                                "suffixes": "pdf"
                            }
                        ]
                    },
                    {
                        "name": "Microsoft Edge PDF Viewer",
                        "description": "Portable Document Format",
                        "mimeTypes": [
                            {
                                "type": "application/pdf",
                                "suffixes": "pdf"
                            },
                            {
                                "type": "text/pdf",
                                "suffixes": "pdf"
                            }
                        ]
                    },
                    {
                        "name": "WebKit built-in PDF",
                        "description": "Portable Document Format",
                        "mimeTypes": [
                            {
                                "type": "application/pdf",
                                "suffixes": "pdf"
                            },
                            {
                                "type": "text/pdf",
                                "suffixes": "pdf"
                            }
                        ]
                    }
                ]
            },
            "sac": {
                "data": {
                    "wpd": true,
                    "ytg": "1fd188f9714ca90a5a10eb2fc306b5eb",
                    "tcg": "_tcg_tcg_val",
                    "xt": "32a115bd05e0f411c5ecd7e285fd36e2"
                }
            },
            "sstot": {
                "data": {
                    "maxTouchPoints": 0,
                    "touchEvent": false,
                    "touchStart": false
                }
            },
            "rev": {
                "data": "Google Inc."
            },
            "sadev": {
                "data": [
                    "chrome"
                ]
            },
            "doc": {
                "data": true
            },
            "drh": {
                "data": true
            },
            "lew": {
                "data": "Google Inc. (Apple)ANGLE (Apple, Apple M1, OpenGL 4.1)"
            },
            "slo": {
                "data": [
                    "location"
                ]
            },
            "pst": {
                "data": [
                    false,
                    false,
                    false
                ]
            }
        },
        "roe": {
            "aup": "3",
            "sep": "3",
            "egp": "3",
            "auh": "3",
            "rew": "3",
            "snh": "3",
            "snih": "3",
            "res": "3",
            "resl": "3",
            "stpn": "3"
        }
    },
    "va8R": "wG3Q",
    "em": {
        "ph": 0,
        "cp": 0,
        "ek": "11",
        "wd": 1,
        "nt": 0,
        "si": 0,
        "sc": 0
    }
    }
  xiyu = JSON.stringify(xiyu).replace(" ", "").replace("'", '"')
  w = AES_Encrypt(randomkey, xiyu)+ RSA_encrypt(randomkey)
  return w
}



// lot_number = 'de023059ed154096bc535dece6904205'
// captcha_id = gt = '0b2abaab0ad3f4744ab45342a2f3d409'
// detail_time = '2024-03-12T13:50:04.645097+08:00'
// distance = 300
// passtime = 1786
// track = [[34,45,67,78],[23, 45, 56, 67]]
// console.log(get_w2(gt, lot_number, detail_time, distance, passtime, track))


