import jwt
import requests
import urllib3, random, hashlib, json, time, copy

from realname.needlogin import LoginByPhone

urllib3.disable_warnings()

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzkyNjE3ODEsImV4cCI6MTc4OTYyOTc4MSwiZGF0YSI6eyJzaW5nbGUiOiJMRDNOSlFZNUdIRlBWTjJHIiwidWlkIjoyNTQyMjYyMiwiYnVzaW5lc3MiOiIxIiwic3lzdGVtX3R5cGUiOiJhbmRyb2lkIiwibWluaV90b2tlbiI6IkxEM05KUVk1R0hGUFZOMkciLCJpZCI6MjU0MjI2MjIsInV1aWQiOjI1NDIyNjIyfSwidG9rZW4iOnsicmVnUnQiOiJhbmRyb2lkIiwidGVuYW50S2V5IjoiWVBaUCIsInRlbmFudElkIjoyNTQyMjYyMiwicGFja2FnZU5hbWUiOiJpby5kY2xvdWQuSDU3NkU2Q0M3IiwidXNlcklkIjoyNTQyMjYyMiwidG9rZW4iOiJMRDNOSlFZNUdIRlBWTjJHIn19.8zfS_xSU9FwzJ52Pltjr8er9k4qIRSK5vzLg5UAe0b0"



class UserBehavior():
    def __init__(self):
        # 初始化 HTTP 客户端
        self.client = urllib3.PoolManager()
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzkyNjE3ODEsImV4cCI6MTc4OTYyOTc4MSwiZGF0YSI6eyJzaW5nbGUiOiJMRDNOSlFZNUdIRlBWTjJHIiwidWlkIjoyNTQyMjYyMiwiYnVzaW5lc3MiOiIxIiwic3lzdGVtX3R5cGUiOiJhbmRyb2lkIiwibWluaV90b2tlbiI6IkxEM05KUVk1R0hGUFZOMkciLCJpZCI6MjU0MjI2MjIsInV1aWQiOjI1NDIyNjIyfSwidG9rZW4iOnsicmVnUnQiOiJhbmRyb2lkIiwidGVuYW50S2V5IjoiWVBaUCIsInRlbmFudElkIjoyNTQyMjYyMiwicGFja2FnZU5hbWUiOiJpby5kY2xvdWQuSDU3NkU2Q0M3IiwidXNlcklkIjoyNTQyMjYyMiwidG9rZW4iOiJMRDNOSlFZNUdIRlBWTjJHIn19.8zfS_xSU9FwzJ52Pltjr8er9k4qIRSK5vzLg5UAe0b0"


    def GetToken(self,phone):
        # 假设 LoginByPhone() 返回的是 token 字符串
        token = LoginByPhone(phone)
        # 动态设置实例属性 self.token 为获取到的值
        setattr(self, 'token', token)
        return token

    def handle(self, phone, draftReasonCode):
        ### 改动点一 ###: 请求方法
        # uri = "/job/v3/manage/draft/save"
        self.GetToken(phone)
        HOST = "http://yupao-test.yupaowang.com"
        post_url = HOST + '/job/v3/manage/draft/save'

        ### 改动点二 ###: 接口参数【建议直接使用抓包工具，获取body参数】；无参数时格式： data = {}
        data = {
            "recruitType": 1,
            "occV2": [{"industry": -1, "occIds": ["505"]}],
            "title": "招聘普工",
            "detail": "招聘普工数名，要求身体健康，服从安排，薪资面议。",
            "mobile": phone,
            "draftReasonCode": draftReasonCode,
            "areaId": 122,
            "location": {
                "longitude": 109.442900,
                "latitude": 19.221641
            },
            "address": "白沙黎族自治县@@@@@海南省白沙黎族自治县"
        }


        response = requests.post(url=post_url, headers=self.configHeader(data), verify=False, json=data)
        if response.status_code != 200 or '"code":0' not in response.text:
            print("接口报错3：" + response.text)
        else:
            print("请求成功：" + response.text)

    def configHeader(self, data):
        sign = getSign(data)

        osReplace = "ANDROID"
        runtimeReplace = "ANDROID"
        packagenameReplace = "io.dcloud.H576E6CC7"

        return {
            'OS': osReplace,
            'runtime': runtimeReplace,
            'business': 'YPZP',
            'osVersion': '15.5',
            'packagename': packagenameReplace,
            'packageversion': '7.2.0',
            'runtimeVersion': '1.21.0',
            'uid': str(self.analysisJwtGetUid()),
            'timestamp': sign['timestamp'],
            'nonce': sign['nonce'],
            'sign': sign['sign'],
            'userrole': '2',
            'appId': "108",
            'token': self.token,
            'channel': "dev"
        }

    def analysisJwtGetUid(self):
        decoded_jwt = jwt.decode(self.token, options={"verify_signature": False})
        uid = decoded_jwt['data'].get('uid')
        if not uid:
            print("token error")
        return uid

    def on_start(self):
        self.token = str(random.choice(token.split("||")))


def getSign(data: dict) -> dict:
    """
    按照 https://w3nu1yaadv.feishu.cn/wiki/wikcnbmdedVBZVHkVyksbLNQM6e 签名
    :param data:
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    nonce = str(random.randint(1, 2 ** 30))
    dataTmp = copy.deepcopy(data)
    if data:
        dataTmp.update({"nonce": nonce, "timestamp": timestamp})
    else:
        dataTmp = {"nonce": nonce, "timestamp": timestamp}

    tmpStr = sortedParams(dataTmp)
    sign = hashlib.sha256(tmpStr.encode('utf-8')).hexdigest()
    return {"timestamp": timestamp, "nonce": nonce, "sign": sign}


# 定义工具函数，请求参数进行字典排序
def sortedParams(params: dict) -> str:
    params = json.dumps(params, sort_keys=True)
    # 秘钥
    params = json.loads(params)
    sb = []
    for key in params:
        v = params[key]
        if isinstance(v, (str, int, float)):
            params[key] = str(v)
        if isinstance(v, bool):
            params[key] = str(v).lower()
        elif isinstance(v, (dict, list)):
            params[key] = json.dumps(v, sort_keys=True, ensure_ascii=False).replace(' ', '')

        sb.append(f'{key}={params[key]}')
    secret = "8k&^$Hsk1?kkcj12^99K1ia"
    return ("&".join(sb)) + '&' + secret




if __name__ == '__main__':
    work = UserBehavior()
    work.handle(13882624156, 1)