import copy
import functools
import hashlib
import random
import time
import random

import requests
import json
from goss import gosslogin

#全局变量
SECRET_SALT = '8k&^$Hsk1?kkcj12^99K1ia'
def check_login_status(_self):
    res = _self.sess.get(url=_self.hostname + r'/uaa/v1/permission/current/user', headers=_self.headers)
    if "用户需要登录" in res.text:
        print("java中台登录失效.........")
        _self.login()
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check_login_status(args[0])
        result = func(*args, **kwargs)
        return result

    return wrapper

class realname():
    def __init__(self):
        # cookies="areaInfo=%7B%22id%22%3A1%2C%22pid%22%3A%22%22%2C%22name%22%3A%22%E5%85%A8%E5%9B%BD%22%2C%22nameA%22%3A%22%EF%BB%BF%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%22%2C%22ltr%22%3A%22quanguo%22%2C%22lv%22%3A1%2C%22adcode%22%3A%22100000%22%7D; HMACCOUNT=C0F8BF315AD73E97; current_identity=2; Hm_lvt_14752563c89f0870e93d2f6ac497f815=1775639310; USERID=25414964; TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzU2MzkzMjksImV4cCI6MTc4NjAwNzMyOSwiZGF0YSI6eyJzaW5nbGUiOiJSRjZGRFQ4RUNFUkdXSDFRIiwidWlkIjoyNTQxNDk2NCwiYnVzaW5lc3MiOiIxIiwic3lzdGVtX3R5cGUiOiJjb21wdXRlciIsIm1pbmlfdG9rZW4iOiJSRjZGRFQ4RUNFUkdXSDFRIiwiaWQiOjI1NDE0OTY0LCJ1dWlkIjoyNTQxNDk2NH0sInRva2VuIjp7InJlZ1J0IjoicGMiLCJ0ZW5hbnRLZXkiOiJZUFpQIiwidGVuYW50SWQiOjI1NDE0OTY0LCJwYWNrYWdlTmFtZSI6InlwLnBjIiwidXNlcklkIjoyNTQxNDk2NCwidG9rZW4iOiJSRjZGRFQ4RUNFUkdXSDFRIn19.9JWwl6UeC772OiLD74uHL5kjTUAnCdZ_XWJPV0CUx_Q; Hm_lpvt_14752563c89f0870e93d2f6ac497f815=1775639336; cookieHostname=beacon-test.yupaowang.com; jwtToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRzIjpbImFkcyIsImFtcyIsImNjb3MiLCJjbXMiLCJjc3MiLCJlZGkiLCJmZWlzaHVoNSIsImhhaXRvdSIsImhlbGxvIiwiamlnb25namlhIiwibW1zIiwicW1zIiwicW1zIiwicmNzIiwic2NybSIsInl1cGFvIiwieXVwYW9kYW9qaWEiLCJ5dXBhb2Rhb2ppYSJdLCJvcGVuSWQiOiJvdV9lNDkwNDI1ZmFhM2I2ZDE0ZWNhMmViNTc1ZmI2ZWM0MSIsInVzZXJOYW1lIjoi5rGk55WqIiwiZXhwIjoxNzc2NDE0NTMwLCJ1c2VySWQiOiI2NzJiN2c2ZCJ9.0esZupTclzbotg33A9IaBWd8AcQZkkcPIu8_uX1F7BA"
        # print(cookies)
        #
        # self.header = {
        #     "accept": "application/json, text/plain, */*",
        #     "accept-encoding": "gzip, deflate, br, zstd",
        #     "accept-language": "zh-CN,zh;q=0.9",
        #     "business": "yupao",
        #     "connection": "keep-alive",
        #     "content-length": "239",
        #     "content-type": "application/json",
        #     "cookie": cookies,
        #     "host": "yupao-test-backend.yupaowang.com",
        #     "origin": "https://goss-test.yupaowang.com",
        #     "referer": "https://goss-test.yupaowang.com/",
        #     "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"macOS"',
        #     "sec-fetch-dest": "empty",
        #     "sec-fetch-mode": "cors",
        #     "sec-fetch-site": "same-site",
        #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        # }
        # self.session = requests.Session()
        self.sess = requests.session()
        self.sess.trust_env = False
        self.hostname = 'https://yupao-test-backend.yupaowang.com'
        self.baseurl = r'https://yupao-test-backend-intranet.yupaowang.com'
        self.userAgent = random.choice([
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {
                "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
            {
                "User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"}
        ])
        self.headers = {'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'content-type': 'application/json',
                        'system_type': 'backend',
                        'Cookie': 'jwtToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRzIjpbIm1tcyIsInl1cGFvIl0sIm9wZW5JZCI6Im91XzhhMGFjMWY3OTFhNTgzNzZmMWJjMDNhZjZhNjExMTY0IiwidXNlck5hbWUiOiLnvZfnm5vmlociLCJleHAiOjE3MjU1MDgwMjAsInVzZXJJZCI6ImQzODcxOTFjIn0.RJ-l_-bKdaTqrpiy4uAoGo5qx_xtqMQ2FgoJbH1rcPc',
                        'apitest': "1"
                        }
        self.login()

    def login(self):
        url = "http://10.16.30.64:5001/user/oauthLdap"
        data = {
            "name": "luoshengwen",
            "pwd": "Lsw979997",
            "username": "android-auto-test",
            "env": "test"
        }
        headers = {"env": "test"}
        print("java中台登录中.........")
        res = self.sess.request(method='POST', url=url, json=data, headers=headers)
        token = res.json()['data']['data']['token'].split("token=")[1]
        cookie = "jwtToken=" + token
        # cookie = "jwtToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRzIjpbImFtcyIsImhlbGxvIiwibW1zIiwieXVwYW8iXSwib3BlbklkIjoib3VfOGEwYWMxZjc5MWE1ODM3NmYxYmMwM2FmNmE2MTExNjQiLCJ1c2VyTmFtZSI6Iue9l-ebm-aWhyIsImV4cCI6MTc2MzQ0NzI3OSwidXNlcklkIjoiZDM4NzE5MWMifQ.6bNS0x5vJ6BRNRfBcSBf8kEgoanqFdbMIvIMFqoBGcw"
        self.headers.update({'Cookie': cookie})

    @my_decorator
    def overRequest(self, *args):
        self.headers.update(self.userAgent)
        return self.sess.request(method='post', url=args[0], json=args[1], headers=self.headers,
                                 allow_redirects=False)


    def sortedParams(self, params=None):
            """递归排序请求参数"""
            if params is None:
                params = {}

            # 先通过JSON序列化反序列化进行第一层排序
            params = json.dumps(params, sort_keys=True)
            params = json.loads(params)

            # 递归处理嵌套结构
            for key in params:
                if params[key] == "" or params[key] is None:
                    params[key] = "null"
                elif not isinstance(params[key], (str, int)):
                    if isinstance(params[key], list):
                        params[key] = sorted(params[key])
                    elif isinstance(params[key], dict):
                        params[key] = self.sortedParams(params[key])
            return params


    def getSign(self, params=None):

        """生成签名并更新到请求头"""
        if params is None:
                params = {}

        params = copy.deepcopy(params)
        # 生成时间戳和随机数
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        nonce = random.randint(1, 2 ** 31)  # 随机数

        # 更新请求头
        self.header.update({
                "timestamp": str(timestamp),
                "nonce": str(nonce)
        })

        # 更新参数
        params.update({
                "timestamp": str(timestamp),
                "nonce": str(nonce)
        })

        # 参数排序
        params = self.sortedParams(params)

        # 拼接参数字符串
        salt_str = ""
        for key, value in params.items():
            salt_str += f"{key}={value}&"

        # 移除可能的空格
        salt_str = salt_str.replace(" ", "")

            # 拼接加密盐并生成签名
        salt_str += SECRET_SALT
        sign = hashlib.sha256(salt_str.encode()).hexdigest()

        # 更新签名到请求头
        self.header.update({"sign": sign})

    """-------------------------------------根据用户ID查询手机号Hash-------------------------------------"""

    def getUserInfoByID(self, user_id):
        """
        :param phone:
        :return:
        """
        url = self.hostname + r"/accountManage/v1/userQuery/queryByCondition"

        data = {
            "userId": user_id,
            "tenantKey": "YPZP",
            "currentPage": 1,
            "pageSize": 10
        }

        res = self.overRequest(url, data)
        # tel_hash = res.json()["data"]["data"][0]["telHash"]
        # # print("******telhash******", tel_hash)
        # return tel_hash
        data = res.json()
        # 假设 data['data']['data'] 是一个列表
        data_list = data.get('data', {}).get('data', [])

        # 安全地遍历列表
        for item in data_list:
            if 'telHash' in item:
                tel_hash = item['telHash']
                # print(f"telHash: {tel_hash}")
                return tel_hash
                # 如果只需要第一个 telHash，可以 break
                # break
            else:
                print("未找到 telHash")
    """------------------------使用hash获取真实号码-----------------------------------------------"""
    def getRealTelByHash(self, user_id):
        """
        :param phone:
        :return:
        """
        url2 = self.hostname + r"/reach/v1/privacyTelUserTel/lookRealTel"
        tel_hash2 = self.getUserInfoByID(user_id)
        # print("****tel_hash2****", tel_hash2)   #打印手机号Hash
        data2 = {
            "telHash": tel_hash2,
            "tenantKey": "YPZP",
            "currentPage": 1,
            "pageSize": 10
        }
        res2 = self.overRequest(url2, data2)

        data = res2.json()
        if data is not None and hasattr(data, 'get'):
            data_dict = data.get('data', {})
            if data_dict is not None and hasattr(data_dict, 'get'):
                tel_real = res2.json()["data"]["tel"]
                if tel_real is not None:
                    # print(tel_real)   #打印真实号码
                    return tel_real
                else:
                    print("HASH检查失败:电话号码未找到")
            else:
                print("HASH检查失败：data 字段为空或无效")
        else:
            print("HASH检查失败：JSON 解析失败或返回 None")


    """-------------------------------------根据手机号查询是否是测试账号-------------------------------------"""

    def checkTelisallow(self, tel2):
        test_phones = ("13882624156", "18482696553")
        if tel2 in test_phones:
            result2 = "true"
            print("手机号在测试白名单")
            return result2
        else:
            result2 = "false"
            print("******手机号不在测试白名单")
            return result2
    # def test(self,user_id):
    #     tel = self.getRealTelByHash(user_id)
    #     result = self.checkTelisallow(tel)
    #     if result == "true":
    #         print("手机号在测试白名单")
    #     else:
    #         print("手机号不在测试白名单")


    # def list_request(self,user_id):
    #     tel = self.getRealTelByHash(user_id)
    #     result = self.checkTelisallow(tel)
    #     if result == "true":
    #         payload = {
    #                 "userId": user_id,
    #                 "tenantKey": "YPZP",
    #                 "nation": "汉",
    #                 "age": 28,
    #                 "sex": 1,
    #                 "idCardFaceUrl": "/r/33ec/108/pr/p/20260410/85794a0eb9c0445d9279c76563bafa14.svg+xml",
    #                 "idCardNumber": "3d58359cdd2fa59f577d886c1c193697",
    #                 "remark": "",
    #                 "idCardName": "汤番"
    #             }
    #         # self.getSign(payload)
    #         # response = self.session.post(url, headers=self.header, data=json.dumps(payload))
    #         url = self.hostname + r'/accountManage/v1/userManage/submitRealName'
    #         response = self.overRequest(url, payload)
    #         print("Status Code:", response.status_code)
    #         print("Response Body:", response.text)
    #     else:
    #         print("没有授权或其他报错")
    def GetRealNameinfo(self,user_id):
        """ 获取实名基础信息及身份证Hash"""
        # tel = self.getRealTelByHash(user_id)
        # result = self.checkTelisallow(tel)
        # if result == "true":
        #     data = {
        #         "userId": user_id,
        #         "tenantKey": "YPZP"
        #     }
        #     if 'Business' in self.headers:
        #         del self.headers['Business']
        #     url = self.hostname + r'/accountManage/v1/userManage/query'
        #     res = self.overRequest(url, data)
        #     # print("获取实名基础信息：",res.json())
        #     return res.json()
        # else:
        #     print("用户未认证")
        data = {
            "userId": user_id,
            "tenantKey": "YPZP"
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/accountManage/v1/userManage/query'
        res = self.overRequest(url, data)
        # print("获取实名基础信息：",res.json())
        return res.json()

    def GetRealidCardNumber(self, idCardNumber):
        """ 身份证Hash获取真实身份证号码"""
        # tel = self.getRealTelByHash(user_id)
        # result = self.checkTelisallow(tel)
        if idCardNumber is not None:
            data = {
                "idCardNumber": idCardNumber
            }
            if 'Business' in self.headers:
                del self.headers['Business']
            url = self.hostname + r'/accountManage/v1/common/idCardCount'
            res = self.overRequest(url, data)
            print("获取实名基础信息：",res.json())
            return res.json()
        else:
            print("身份证号码错误")
    def updateRealNameinfo(self,user_id):
        """ 修改实名基础信息"""
        tel = self.getRealTelByHash(user_id)
        result = self.checkTelisallow(tel)

        if result == "true":
            BashInfo = self.GetRealNameinfo(user_id)
            # print("获取实名基础信息：", BashInfo)
            if BashInfo["data"] is not None:
                IdCardNumber = BashInfo["data"]["realNameInfo"]["idCardNumber"]
                Nation = BashInfo["data"]["realNameInfo"]["nation"]
                Age = BashInfo["data"]["realNameInfo"]["age"]
                Sex = BashInfo["data"]["realNameInfo"]["sex"]
                IdCardName = BashInfo["data"]["realNameInfo"]["idCardName"]
                data = {
                        "userId": user_id,
                        "tenantKey": "YPZP",
                        "nation": Nation,
                        "age": Age,
                        "sex": Sex,
                        "idCardFaceUrl": "/r/33ec/108/pr/p/20260410/85794a0eb9c0445d9279c76563bafa14.svg+xml",
                        "idCardNumber": IdCardNumber,
                        "remark": "",
                        "idCardName": IdCardName
                    }
                if 'Business' in self.headers:
                    del self.headers['Business']
                url = self.hostname + r'/accountManage/v1/userManage/submitRealName'
                res = self.overRequest(url, data)
                print("实名结果：", res.json())
                return res.json()
            else:
                print("获取不到上一次的认证信息")
        else:
            print("实名前置动作未完成，不能认证，请先在APP或小程序提交一次")

    def updateFaceInfo(self,user_id):
        """
        修改人脸信息
        :param userId:
        :param checkStatus: - 2 审核成功 -3 审核失败
        :return:
        """
        tel = self.getRealTelByHash(user_id)
        result = self.checkTelisallow(tel)
        if result == "true":
            self.updateRealNameinfo(user_id)
            data = {
                    "faceUrl": "/r/845a/108/pr/p/20260412/44d2d3c32ecc419e8e89c4c745c887de.jpeg",
                    "tenantKey": "YPZP",
                    "userId": user_id
                }
            if 'Business' in self.headers:
                del self.headers['Business']
            url = self.hostname + r'/accountManage/v1/userManage/submitFace'
            res = self.overRequest(url, data)
            print("人脸结果：", res.json())
            return res.json()
        else:
            print("人脸前置动作未完成不能认证")

    def updateEnterpriseInfo(self,user_id):
        """
        修改企业信息
        :param userId:
        :param checkStatus: - 2 审核成功 -3 审核失败
        :return:
        """
        tel = self.getRealTelByHash(user_id)
        result = self.checkTelisallow(tel)
        if result == "true":
            self.updateFaceInfo(user_id)
            data = {
                "name": "资中鱼泡科技有限公司",
                "socialCreditCode": "91511025MAEFK49G4D",
                "legalPerson": "周峰",
                "enterpriseType": 1,
                "type": 5,
                "enterpriseStatus": 2,
                "failTypeList": [],
                "emailJoinSwitch": "true",
                "enterpriseEmail": "@yupaowang.com",
                "remark": "",
                "busLicenseUrl": "/r/55eb/108/pr/p/20260412/c741c06ec7be4ee5ade3b39a75bd1c0d.jpeg",
                "employmentCertificationUrl": "",
                "materialUrl": "",
                "legalIdCardUrl": "",
                "legalSignCertificateUrl": "",
                "userId": user_id,
                "tenantKey": "YPZP"
            }
            if 'Business' in self.headers:
                del self.headers['Business']
            url = self.hostname + r'/accountManage/v1/userManage/submitEnterprise'
            res = self.overRequest(url, data)
            print("企业结果：", res.json())
            return res.json()
        else:
            print("企业前置动作未完成不能认证")

    def updateTwoElementRealNameinfo(self,user_id):
        """ 修改实名基础信息"""
        tel = self.getRealTelByHash(user_id)
        result = self.checkTelisallow(tel)

        if result == "true":
            data = {
                "userId": 25422622,
                "idCardName": "汤番",
                "idCardNumber": "511621199706147079"
            }
            if 'Business' in self.headers:
                del self.headers['Business']
            url = self.hostname + r'/accountManage/v1/authentication/twoElement'
            res = self.overRequest(url, data)
            print("二要素结果：", res.json())
            return res.json()
        else:
            print("二要素认证前置动作未完成，不能认证")

    def close(self):
            """关闭会话"""
            self.session.close()

def submit_realname():
    """主函数"""
    # 创建请求客户端
    client = realname()

    try:
        # 执行单次请求
        client.list_request()

        # 如果需要循环执行，可以取消下面的注释
        # import time
        # while True:
        #     client.list_request()
        #     time.sleep(1)  # 每秒执行一次

    finally:
        # 关闭会话
        client.close()


if __name__ == "__main__":
    RealNameVerifyControl = realname()
    # RealNameVerifyControl.updateRealNameinfo(1)
    # RealNameVerifyControl.updateFaceInfo(25422622)
    # RealNameVerifyControl.updateEnterpriseInfo(25422622)
    # RealNameVerifyControl.GetRealNameinfo(25422622)
    # RealNameVerifyControl.GetRealidCardNumber('3d58359cdd2fa59f577d886c1c193697')
    RealNameVerifyControl.updateTwoElementRealNameinfo(25422622)
