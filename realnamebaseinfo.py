#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: swluo
import functools
import json
import random
import time

import requests
from jsonpath_ng import parse



def check_login_status(_self):
    res = _self.sess.get(url=_self.hostname + r'/uaa/v1/permission/current/user', headers=_self.headers)
    if "用户需要登录" in res.text:
        print("java中台登录失效.........")
        _self.login()


# def check_login_status(result):
#     return True if "用户需要登录" in result else False


def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check_login_status(args[0])
        result = func(*args, **kwargs)
        return result

    return wrapper


#
# def my_decorator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if result.json()['message'] != "请求成功":
#             args[0].login()
#             result = func(*args, **kwargs)
#         return result
#
#     return wrapper


class realname:
    def __init__(self):

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
                        'Cookie': 'jwtToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRzIjpbImFtcyIsImhlbGxvIiwibW1zIiwieXVwYW8iXSwib3BlbklkIjoib3VfOGEwYWMxZjc5MWE1ODM3NmYxYmMwM2FmNmE2MTExNjQiLCJ1c2VyTmFtZSI6Iue9l-ebm-aWhyIsImV4cCI6MTc3NDQwNTE2MywidXNlcklkIjoiZDM4NzE5MWMifQ.mcTNOypmekTWZLIz97QYEIhExQ12xJnp79FfSSS7OeM',
                        'apitest': "1"
                        }
        print("原始的ldapCookie:", self.headers.get('Cookie'))
        self.login()

    def login(self):
        url = "http://10.16.30.64:5001/user/oauthLdap"
        data = {
            "name": "tangfan",
            "pwd": "YPad666",
            "username": "android-auto-test",
            "env": "test"
        }
        headers = {"env": "test"}
        print("java中台登录中.........")
        res = self.sess.request(method='POST', url=url, json=data, headers=headers)
        # print("登录headers：", headers)
        # print("登录data：", data)
        # print("登录res.........", res.json())
        token = res.json()['data']['data']['token'].split("token=")[1]
        cookie = "jwtToken=" + token
        # cookie = "jwtToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRzIjpbImFtcyIsImhlbGxvIiwibW1zIiwieXVwYW8iXSwib3BlbklkIjoib3VfOGEwYWMxZjc5MWE1ODM3NmYxYmMwM2FmNmE2MTExNjQiLCJ1c2VyTmFtZSI6Iue9l-ebm-aWhyIsImV4cCI6MTc2MzQ0NzI3OSwidXNlcklkIjoiZDM4NzE5MWMifQ.6bNS0x5vJ6BRNRfBcSBf8kEgoanqFdbMIvIMFqoBGcw"
        self.headers.update({'Cookie': cookie})

    @my_decorator
    def overRequest(self, *args):
        self.headers.update(self.userAgent)
        return self.sess.request(method='post', url=args[0], json=args[1], headers=self.headers, allow_redirects=False)


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
        print("获取实名基础信息：", res.json())
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
    # RealNameVerifyControl.updateRealNameinfo(31297817)
    RealNameVerifyControl.updateFaceInfo(25422622)
    # RealNameVerifyControl.updateEnterpriseInfo(31297817)
    # RealNameVerifyControl.GetRealNameinfo(25422622)
    # RealNameVerifyControl.GetRealidCardNumber('3d58359cdd2fa59f577d886c1c193697')
    # RealNameVerifyControl.updateTwoElementRealNameinfo(31297817)
    # RealNameVerifyControl.login()
    # RealNameVerifyControl.GetRealidCardNumber(511621199706147079)
