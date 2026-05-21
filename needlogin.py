# -*- coding: utf-8 -*-
import random
import time, copy, hashlib
import requests
import queue
import json

q = queue.Queue()
for i in range(1500000, 2000000):
    q.put(i)


# host = "http://yupao-master-intranet.yupaowang.com"
# host = "http://yupao-test-intranet.yupaowang.com"
def get_gmt_time():
    """
    获取时间
    :return:时间戳
    """
    return int(round(time.time() * 1000))


def get_sign2(data={}):
    """
    java接口鉴权加密
    :param data:
    :return: json
    """
    timestamp = str(get_gmt_time())
    nonce = str(random.randint(1, 2 ** 30))
    secretSalt = '8k&^$Hsk1?kkcj12^99K1ia'  # 测试环境
    # secretSalt = "*js1(Uc_m12j%hsn#1o%cn1"  # 预发布及正式
    datatmp = copy.deepcopy(data)
    if data:
        datatmp.update({"nonce": nonce, "timestamp": timestamp})
    else:
        datatmp = {"nonce": nonce, "timestamp": timestamp}
    tmpdict = datatmp
    datasort = sorted(datatmp)
    tmpstr = ''
    for key in datasort:
        if tmpdict[key]:
            if tmpstr:
                tmpstr += '&'
            tmpstr += str(key) + '=' + str(tmpdict[key])
    tmpstr = tmpstr.replace("'", "\"").replace(" ", "")
    tmpstr += '&' + secretSalt
    # print(tmpstr)
    sign = hashlib.sha256()
    sign.update(tmpstr.encode())
    headers_sign = {"timestamp": timestamp, "nonce": nonce, "sign": sign.hexdigest()}
    return headers_sign


HOST = "http://yupao-test.yupaowang.com"


def get_token():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzkyNjE0NjMsImV4cCI6MTc4OTYyOTQ2MywiZGF0YSI6eyJzaW5nbGUiOiI1VFdCWUxSRzZWV1hOWVhDIiwidWlkIjoyNTQyMjYyMiwiYnVzaW5lc3MiOiIxIiwic3lzdGVtX3R5cGUiOiJhbmRyb2lkIiwibWluaV90b2tlbiI6IjVUV0JZTFJHNlZXWE5ZWEMiLCJpZCI6MjU0MjI2MjIsInV1aWQiOjI1NDIyNjIyfSwidG9rZW4iOnsicmVnUnQiOiJhbmRyb2lkIiwidGVuYW50S2V5IjoiWVBaUCIsInRlbmFudElkIjoyNTQyMjYyMiwicGFja2FnZU5hbWUiOiJpby5kY2xvdWQuSDU3NkU2Q0M3IiwidXNlcklkIjoyNTQyMjYyMiwidG9rZW4iOiI1VFdCWUxSRzZWV1hOWVhDIn19.wb-Vqh7t_Al4aLcNnsBRRyPaEP9jg6UDd5ZmOMRzrUE"
    return token


def build_headers(token):
    return {
        'business': 'YPZP',
        'runtime': 'ANDROID',
        'runtimeVersion': '13',
        'os': 'ADNRIOD',
        'OSVersion': '13',
        'packageName': 'io.dcloud.H576E6CC7',
        'packageVersion': '6.1.0',
        'occversion': '2',
        'Content-Type': 'application/json',
        'apitest': '1',
        'token': token
    }


def GetCode(headers,phone):
    """发送验证码接口"""
    post_url = HOST + '/reach/v1/verifyCode/loginIgnore/send'
    body = {
        "biz": "login",
        "tel": phone
    }
    sign = get_sign2(body)
    headers.update({"timestamp": sign['timestamp'], "nonce": sign['nonce'], "sign": sign['sign']})
    response = requests.post(url=post_url, headers=headers, verify=False, json=body)
    if response.status_code != 200 or '"code":0' not in response.text:
        print("接口报错：" + response.text)
    else:
        print("请求成功：" + response.text)
        codetoken = response.json()['data']['verifyToken']
        return codetoken

def LoginByPhone(phone):
    """登录接口"""
    token = get_token()
    headers = build_headers(token)
    verifyToken = GetCode(headers, phone)
    print(verifyToken)
    post_url = HOST + '/account/v1/login/codeLogin'
    body = {
      "code": "9876",
      "hasSim": "true",
      "shareReq": {
        "refTenantId": "",
        "shareSource": "",
        "trackSeed": ""
      },
      "tel": phone,
      "verifyToken": verifyToken
    }
    sign = get_sign2(body)
    headers.update({"timestamp": sign['timestamp'], "nonce": sign['nonce'], "sign": sign['sign']})
    response = requests.post(url=post_url, headers=headers, verify=False, json=body)
    if response.status_code != 200 or '"code":0' not in response.text:
        print("接口报错2：" + response.text)
    else:
        print("请求成功：" + response.text)
        token = response.json()['data']['token']
        return token


# def Savedraft(phone,draftReasonCode):
#     """登录接口"""
#     token = LoginByPhone(phone)
#     headers = build_headers(token)
#     headers.update({'token': token})
#     # print("Savedraft的headers:", headers)
#     # headers = {
#     #   "business": "YPZP",
#     #   "runtime": "ANDROID",
#     #   "runtimeVersion": "13",
#     #   "os": "ADNRIOD",
#     #   "OSVersion": "13",
#     #   "packageName": "io.dcloud.H576E6CC7",
#     #   "packageVersion": "6.1.0",
#     #   "occversion": "2",
#     #   "Content-Type": "application/json",
#     #   "apitest": "1",
#     #   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzkxODYxODQsImV4cCI6MTc4OTU1NDE4NCwiZGF0YSI6eyJzaW5nbGUiOiJTN0VENjNTQ1dEQlk0NDY2IiwidWlkIjoyNTQyMjYyMiwiYnVzaW5lc3MiOiIxIiwic3lzdGVtX3R5cGUiOiJhbmRyb2lkIiwibWluaV90b2tlbiI6IlM3RUQ2M1NDV0RCWTQ0NjYiLCJpZCI6MjU0MjI2MjIsInV1aWQiOjI1NDIyNjIyfSwidG9rZW4iOnsicmVnUnQiOiJhbmRyb2lkIiwidGVuYW50S2V5IjoiWVBaUCIsInRlbmFudElkIjoyNTQyMjYyMiwicGFja2FnZU5hbWUiOiJpby5kY2xvdWQuSDU3NkU2Q0M3IiwidXNlcklkIjoyNTQyMjYyMiwidG9rZW4iOiJTN0VENjNTQ1dEQlk0NDY2In19.zGIimKUulCdJVOyUZXHoOqiMjG36N-lyFOmYkD4ARaY"
#     # }
#
#     post_url = HOST + '/job/v3/manage/draft/save'
#
#     payload = {
#         "recruitType": 1,
#         "occV2": [{"industry": -1, "occIds": ["505"]}],
#         "title": "招聘普工",
#         "detail": "招聘普工数名，要求身体健康，服从安排，薪资面议。",
#         "mobile": phone,
#         "draftReasonCode": draftReasonCode,
#         "areaId": 122,
#         "address": "白沙黎族自治县@@@@@海南省白沙黎族自治县"
#     }
# #        "location": {"longitude": "109.442900", "latitude": "19.221641"
#     print("Savedraft的body：", json.dumps(payload, ensure_ascii=False))
#     sign = get_sign2(payload)
#     headers.update({"timestamp": sign['timestamp'], "nonce": sign['nonce'], "sign": sign['sign']})
#     print("Savedraft的headers：", headers)
#     response = requests.post(url=post_url, headers=headers, verify=False, json=payload)
#     if response.status_code != 200 or '"code":0' not in response.text:
#         print("接口报错3：" + response.text)
#     else:
#         print("请求成功：" + response.text)


if __name__ == "__main__":
    LoginByPhone(18482696553)
    # Savedraft(13882624156, 1)