#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: swluo
import functools
import json
import random
import time

import requests



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


class WorkerMiddleControls:
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
        return self.sess.request(method='post', url=args[0], json=args[1], headers=self.headers, allow_redirects=False)

    """-------------------------------------积分操作-------------------------------------"""

    def integralDivert(self, data):
        url = f"{self.hostname}/integral/manage/v1/transferIntegral"
        if 'Business' in self.headers:
            del self.headers['Business']
        # 积分转移
        if data['type'] == 1:
            integral = data['integral']
            userId = self.getUserInfoByPhone(data['phone1'])[0]
            targetUserId = self.getUserInfoByPhone(data['phone2'])[0]
            if integral == '全部':
                integral = self.getUserInfoByPhone(data['phone1'])[1]
            data = {'userId': userId, 'targetUserId': targetUserId, "integral": integral,
                    "remark": '自动化测试'}
            res = self.overRequest(url, data)
            # print(res.json())
            return res
        else:  # 补满逻辑
            integral = data['integral']
            userId = self.getUserInfoByPhone(data['phone1'])[0]
            targetUserId = self.getUserInfoByPhone(data['phone2'])[0]
            phone1_integral = self.getUserInfoByPhone(data['phone1'])[1]
            phone2_integral = self.getUserInfoByPhone(data['phone2'])[1]
            if int(integral) > int(phone2_integral) and int(phone1_integral) >= int(integral) - int(phone2_integral):
                data = {'userId': userId, 'targetUserId': targetUserId,
                        "integral": int(integral) - int(phone2_integral),
                        "remark": '自动化测试'}
                res = self.overRequest(url, data)
                # print(res.json())
                return res
            else:
                return {"code": 200, "msg": "无需转移积分"}

    """-------------------------------------招工置顶-------------------------------------"""

    def getJobTobInfo(self, userId):
        """
        获取置顶的招工信息
        :param userId:
        :return:
        """
        url = self.hostname + r'/member/v1/rightPin/list'
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "uid": userId,
            "infoType": 0
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        res = self.overRequest(url, data)
        print("getJobTobInfo+++++++++++++:" + str(res.json()))
        if res.json()['data']['data'][0]:
            info_id = json.loads(res.text)['data']['data'][0]['infoId']
            top_id = json.loads(res.text)['data']['data'][0]['id']
            return info_id, top_id
        else:
            return "接口请求失败......"

    def getPointValue(self, top_id):
        """
        获取招工置顶消耗积分
        :param top_id:
        :return:
        """
        data = {
            "rightId": top_id
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/member/v1/rightPin/remainIntegral'
        res = self.overRequest(url, data)
        if json.loads(res.text)['message'] == '请求成功':
            points = res.json()["data"]["totalNum"]
            return points
        else:
            return '当前无正处于置顶权益的招工信息'

    def topIntegralOut(self, userId):
        """
        招工置顶积分退还
        :param userId:
        :return:
        """
        info_id, top_id = self.getJobTobInfo(userId)
        points = self.getPointValue(top_id)
        data = {
            "rightId": top_id,
            "refundNum": points
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/member/v1/rightPin/refund'
        res = self.overRequest(url, data)
        return res.text

    """--------------------------------营销中台退积分审核--------------------------------"""

    def handlerRefundReview(self, msg, res, orderNo, checkId):
        if res.json()['message'] != "请求成功":
            msg.append({orderNo: "申请退积分失败", "checkId": checkId, "orderNo": orderNo})
        else:
            time.sleep(2)
            msg.append({orderNo: self.refundReview(checkId), "checkId": checkId, "orderNo": orderNo})

    def refundReview(self, checkId):
        if checkId:
            if self.specifyAllocation(checkId):
                if self.agreeRefund(checkId):
                    return "退款成功"
                else:
                    return "退款失败"
            else:
                return "指定分配失败"
        else:
            return "订单id获取异常，退款失败"

    def specifyAllocation(self, checkId):
        data = {
            "bizId": checkId,
            "projectId": 1210,
            "nodeId": 10011
        }
        url = self.hostname + r'/audit/v1/audit/claimTargetTask'
        self.headers.update({"Business": "mms"})
        res = self.overRequest(url, data)
        claimNum = res.json()["data"]["claimNum"]
        return claimNum == 1

    def agreeRefund(self, checkId):
        data = {
            "bid": checkId,
            "projectId": 1210,
            "nodeId": 10011,
            "resultType": 2
        }
        url = self.hostname + r'/audit/v1/audit/submitResult'
        self.headers.update({"Business": "mms"})
        res = self.overRequest(url, data)
        result = res.json()["data"]["result"]
        return result == 1

    """-------------------------------------加急招-------------------------------------"""

    def urgentJobList(self, userId):
        """
        获取加急招订单列表
        :param userId:
        :return:
        """
        data = {
            "userId": userId,
            "bizType": "YUPAO_URGENT_HIRING",
            "currentPage": 1,
            "pageSize": 15,
            "orderStatus": "PAY_SUCCESS"
        }
        self.headers.update({"Business": "mms"})
        url = self.hostname + r'/trade/v2/orderCenter/orderList'
        res = self.overRequest(url, data)
        refundStatus = json.loads(res.text)['data']['data'][0]['refundStatus']
        # 校验加急招订单状态-->
        if refundStatus == "UN_REFUND":
            orderNo = json.loads(res.text)['data']['data'][0]['orderNo']
            refundPrice = json.loads(res.text)['data']['data'][0]['totalPrice']
            checkId = json.loads(res.text)['data']['data'][0]['id']
            return orderNo, refundPrice, checkId
        else:
            return {'msg': f'{userId}账户无处于加急招的招工信息'}

    def urgentJobOut(self, userId):
        """
        加急招退积分
        :param userId:
        :return:
        """
        try:
            msg = []
            orderNo, refundPrice, checkId = self.urgentJobList(userId)
            data = {
                "orderNo": orderNo,
                "refundPrice": refundPrice,
                "refundRemark": "自动化测试",
                "refundType": "ALL_REFUND",
                "refundGoodsNum": "1",
                "replay": "自动化测试"
            }
            self.headers.update({"Business": "mms"})
            url = self.hostname + r'/trade/v1/refund/order'
            res = self.overRequest(url, data)
            self.handlerRefundReview(msg, res, orderNo, checkId)
            return res.text
        except:
            return {'msg': f'{userId}账户无处于加急招的招工信息'}

    """-------------------------------------聊一聊-------------------------------------"""

    def getChatOrderNo(self, userId):
        """
        获取B端聊一聊次卡购买订单编号
        :param userId:
        :return:
        """
        orderList = []
        data = {
            "userId": userId,
            "currentPage": 1,
            "pageSize": 15,
            "orderStatus": "PAY_SUCCESS",
            "refundStatus": "UN_REFUND",
            "bizType": "YUPAO_B_CHAT_CARD"
        }
        url = self.hostname + r'/trade/v2/orderCenter/orderList'
        self.headers.update({"Business": "mms"})
        res = self.overRequest(url, data)
        orderData = res.json()['data']['data']
        if orderData:
            for order in orderData:
                orderList.append([order['orderNo'], order['orderPrice'], order['id']])
            return orderList
        else:
            return {'msg': f'{userId}账户无处于聊一聊权益中的订单'}

    def userChatPointOut(self, userId):
        """
        B端聊一聊次卡退费
        :param userId:
        :return:
        """
        orderList = self.getChatOrderNo(userId)
        msg = []
        if isinstance(orderList, list):
            for order in orderList:
                orderNo = order[0]
                orderPrice = order[1]
                orderId = order[2]
                data = {
                    "orderNo": orderNo,
                    "refundPrice": orderPrice,
                    "refundRemark": "自动化测试",
                    "refundType": "ALL_REFUND",
                    "refundGoodsNum": "1",
                    "reply": "自动化测试"
                }
                url = self.hostname + r'/trade/v1/refund/order'
                self.headers.update({"Business": "mms"})
                res = self.overRequest(url, data)
                msg.append({orderNo: res.json()['message']})
                self.handlerRefundReview(msg, res, orderNo, orderId)
            return msg
        else:
            return f'{userId}不存在处于聊一聊权益中的订单编号'

    """-------------------------------------找活名片-------------------------------------"""

    def getResumeList(self):
        """
        获取正在找活状态的简历信息列表
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "workStatus": 1,
            "checkStatus": 2
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeSub/pageQuery'
        res = self.overRequest(url, data)
        print("getResumeList+++++++++++:" + str(res.json()))
        uuid = res.json()['data']['data'][0]['uuid']
        return uuid

    def getResumeId(self, userId):
        """
        获取找活名片ID
        :param userId:
        :return:
        """
        data = {
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeMainData/basicData'

        res = self.overRequest(url, data).json()
        if res['data']['basicInfo']:
            resumeId = res['data']['basicInfo']['basic']['id']
            return resumeId
        else:
            return {f'用户：{userId}不存在找活名片'}

    def getResumeUuid(self, userId):
        """
        获取找活名片ID
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeSub/pageQuery'

        res = self.overRequest(url, data).json()
        if res['data']['data']:
            uuid = res['data']['data'][0]['uuid']
            return uuid
        else:
            return {f'用户：{userId}不存在找活名片'}

    def getResumeTopId(self, userId):
        """
        获取简历置顶列表
        :param userId:
        :return:
        """
        resumeId = self.getResumeId(userId)
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "infoId": resumeId,
            "infoType": 1,
            "uid": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r"/member/v1/rightPin/list"

        res = self.overRequest(url, data)
        topList = res.json()['data']['data']
        for info in topList:
            if info['pinStatus'] != 6:
                return info['id']
            else:
                return None

    def getResumePoints(self, topId):
        """
        获取简历退还积分
        :param topId:
        :return:
        """
        data = {
            "rightId": topId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r"/member/v1/rightPin/remainIntegral"
        res = self.overRequest(url, data)
        if res.json()['message'] == "请求成功":
            resumePoints = res.json()['data']['totalNum']
            return resumePoints
        else:
            return None

    def resumeTopIntegralReturn(self, userId):
        """
        简历置顶退积分
        :param userId:
        :return:
        """
        topId = self.getResumeTopId(userId)
        resumePoints = self.getResumePoints(topId)
        if 'Business' in self.headers:
            del self.headers['Business']
        if topId and resumePoints:
            data = {
                "rightId": topId,
                "refundNum": int(resumePoints)
            }

            url = self.hostname + r"/member/v1/rightPin/refund"
            res = self.overRequest(url, data)
            return res.json()
        else:
            return {"msg": "无处于置顶加急中的简历"}

    def getResumeCheckId(self, userId):
        """
        获取找活名片审核ID
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeSub/pageQuery'
        res = self.overRequest(url, data).json()
        print("res+++++++++++++++++++++: " + str(res['message']))
        if res['data']['data']:
            checkId = res['data']['data'][0]['id']
            return checkId
        else:
            return {f'用户：{userId}不存在找活名片'}

    def updateResumeCheckStatus(self, userId, checkStatus):
        """
        审核找活名片
        :param userId:
        :param checkStatus: - 2 审核成功 -3 审核失败
        :return:
        """
        checkId = self.getResumeCheckId(userId)
        if int(checkStatus) == 3:
            data = {
                "id": checkId,
                "checkStatus": int(checkStatus),
                "templateId": 65
            }
        else:
            data = {
                "id": checkId,
                "checkStatus": int(checkStatus),
            }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeSub/updateCheckStatus'
        res = self.overRequest(url, data)
        return res.json()

    """-------------------------------------名片刷新-------------------------------------"""

    def getAutoRefreshOrderId(self, userId):
        """
        获取连续刷新订单号
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "uid": userId,
            "refreshStatus": [
                1,
                2,
                0
            ],
            "infoType": 1
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/member/v1/autoRefresh/pageQuery'

        res = self.overRequest(url, data)
        orderIdList = [orderData["id"] for orderData in res.json()["data"]["data"]]
        payNumList = [payNumData["payNum"] for payNumData in res.json()["data"]["data"]]
        return orderIdList, payNumList

    def autoRefreshReturn(self, userId):
        """
        连续刷新退积分
        :param userId:
        :return:
        """
        orderIdList, payNumList = self.getAutoRefreshOrderId(userId)
        if orderIdList and payNumList:
            for i in range(len(orderIdList)):
                data = {
                    "rightId": orderIdList[i],
                    "refundNum": payNumList[i]
                }
                if 'Business' in self.headers:
                    del self.headers['Business']
                url = self.hostname + r"/member/v1/autoRefresh/refund"

                self.overRequest(url, data)
            return {userId: '已退还连续刷新积分消耗'}

        else:
            return {userId: '未连续刷新简历'}

    """-------------------------------------项目经验-------------------------------------"""

    def getProjectExperienceCheckId(self, userId):
        """
        获取项目经验
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeProjectExperience/pageQuery'
        res = self.overRequest(url, data)
        projectList = res.json()['data']['data']
        if projectList:
            checkId = projectList[0]['id']
            return checkId
        else:
            return {"code": 200, "msg": "当前账号无项目经验"}

    def projectExperienceUpdateCheckStatus(self, userId, checkStatus):
        """
        审核
        :param userId:
        :param checkStatus: - 2 审核成功 -3 审核失败
        :return:
        """
        checkId = self.getProjectExperienceCheckId(userId)
        if checkStatus == 3:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
                "failTemplateId": 79,
                "operator": "",
                "updatedBy": ""
            }
        else:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
                "operator": "",
                "updatedBy": ""
            }
        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/resume/v1/resumeProjectExperience/updateCheckStatus'
        res = self.overRequest(url, data)
        return res.json()

    """-------------------------------------面试视频-------------------------------------"""

    def getResumeVideoCheckStatusId(self, userId):
        """
        获取找活视频审核ID
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeVideo/pageQuery'
        res = self.overRequest(url, data)
        resumeVideoList = res.json()['data']['data']
        if resumeVideoList:
            checkId = resumeVideoList[0]['id']
            return checkId
        else:
            return {"code": 200, "msg": "当前账号无找活视频"}

    def resumeVideoUpdateCheckStatus(self, userId, checkStatus):
        """
        审核找活视频
        :param userId:
        :param checkStatus: -2 审核成功 -3 审核失败
        :return:
        """
        checkId = self.getResumeVideoCheckStatusId(userId)
        if checkStatus == 3:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
                "failTemplateId": 68
            }
        else:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
            }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/resumeVideo/changeCheckStatus'
        res = self.overRequest(url, data)
        return res.json()

    """-------------------------------------教育经历-------------------------------------"""

    def getEduExpCheckStatusId(self, userId):
        """
        获取教育经历审核ID
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/resume/v1/eduExp/pageQuery'
        res = self.overRequest(url, data)
        eduExpList = res.json()['data']['data']
        if eduExpList:
            checkId = eduExpList[0]['id']
            return checkId
        else:
            return {"code": 200, "msg": "当前账号无教育经历"}

    def eduExpUpdateCheckStatus(self, userId, checkStatus):
        """
        审核教育经历
        :param userId:
        :param checkStatus: -2 审核成功 -3 审核失败
        :return:
        """
        checkId = self.getEduExpCheckStatusId(userId)
        if checkStatus == 3:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
                "failTemplateId": 68
            }
        else:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
            }

        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/resume/v1/eduExp/updateCheckStatus'
        res = self.overRequest(url, data)
        return res.json()

    def getEduExpTask(self):
        """
        获取已分配的教育经历审核任务
        :return:
        """
        data = {
            "projectId": 1219,
            "nodeId": 10364
        }
        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/audit/v1/audit/queryAuditorTasks'

        res = self.overRequest(url, data)
        return res.json()

    def eduExpTaskDistribute(self, userId):
        """
        教育审核任务分配
        :param userId:
        :return:
        """
        checkId = self.getEduExpCheckStatusId(userId)
        data = {
            "bizId": checkId,
            "projectId": 1219,
            "nodeId": 10364
        }
        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/audit/v1/audit/claimTargetTask'
        res = self.overRequest(url, data)
        return res.json()

    def eduExpTaskUpdateCheckStatus(self, userId, checkStatus):
        """
        通过分配任务审核教育经历
        :param userId:
        :return:
        """
        checkId = self.getEduExpCheckStatusId(userId)
        if checkStatus == 2:
            data = {
                "projectId": 1219,
                "bid": checkId,
                "resultType": checkStatus
            }
        else:
            data = {
                "projectId": 1219,
                "bid": checkId,
                "resultType": checkStatus,
                "failInfo": {
                    "failReason": "您好！您填写的学校名称非正确信息，请您核实后上传真实有效的信息。如有疑问请致电鱼泡网客服电话400-838-1888进行咨询。",
                    "failTemplateId": 336,
                    "failFields": [],
                    "failSuggestions": {}
                }
            }
        url = self.hostname + r'/audit/v1/audit/submitResult'
        if 'Business' in self.headers:
            del self.headers['Business']

        res = self.overRequest(url, data)
        print("workExpTaskDistribute+++++++++++++++++++:" + str(res.json()))

        return res.json()

    """-------------------------------------工作经历-------------------------------------"""

    def getWorkExpCheckStatusId(self, userId):
        """
        获取工作经历审核ID
        :param userId:
        :return:
        """
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "userId": userId
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/resume/v1/workExp/pageQuery'
        res = self.overRequest(url, data)
        print("getWorkExpCheckStatusId+++++++++++++:" + str(res.json()))
        workExpList = res.json()['data']['data']
        if workExpList:
            checkId = workExpList[0]['id']
            return checkId
        else:
            return {"code": 200, "msg": "当前账号无工作经历"}

    def workExpUpdateCheckStatus(self, userId, checkStatus):
        """
        审核工作经历
        :param userId:
        :param checkStatus: -2 审核成功 -3 审核失败
        :return:
        """
        checkId = self.getWorkExpCheckStatusId(userId)
        if checkStatus == 3:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
                "failTemplateId": 68
            }
        else:
            data = {
                "id": checkId,
                "checkStatus": checkStatus,
            }

        if 'Business' in self.headers:
            del self.headers['Business']

        url = self.hostname + r'/resume/v1/workExp/updateCheckStatus'
        res = self.overRequest(url, data)
        return res.json()

    def getWorkExpTask(self):
        """
        获取已分配的工作经历审核任务
        :return:
        """
        data = {
            "projectId": 1220,
            "nodeId": 10365
        }
        url = self.hostname + r'/audit/v1/audit/queryAuditorTasks'
        if 'Business' in self.headers:
            del self.headers['Business']

        res = self.overRequest(url, data)
        return res.json()

    def workExpTaskDistribute(self, userId):
        """
        工作审核任务分配
        :param checkId:
        :return:
        """
        checkId = self.getWorkExpCheckStatusId(userId)
        data = {
            "bizId": checkId,
            "projectId": 1220,
            "nodeId": 10365
        }
        if 'Business' in self.headers:
            del self.headers['Business']
        url = self.hostname + r'/audit/v1/audit/claimTargetTask'
        res = self.overRequest(url, data)
        return res.json()

    def workExpTaskUpdateCheckStatus(self, userId, checkStatus):
        """
        通过分配任务审核工作经历
        :param userId:
        :return:
        """
        checkId = self.getWorkExpCheckStatusId(userId)
        if checkStatus == 2:
            data = {
                "projectId": 1220,
                "bid": checkId,
                "resultType": checkStatus
            }
        else:
            data = {
                "projectId": 1220,
                "bid": checkId,
                "resultType": checkStatus,
                "failInfo": {
                    "failReason": "您好！您填写的公司名称非正确信息，请您核实后上传真实有效的信息。如有疑问请致电鱼泡网客服电话400-838-1888进行咨询。",
                    "failTemplateId": 339,
                    "failFields": [],
                    "failSuggestions": {}
                }
            }
        url = self.hostname + r'/audit/v1/audit/submitResult'
        if 'Business' in self.headers:
            del self.headers['Business']
        res = self.overRequest(url, data)
        return res.json()

    """-------------------------------------会员服务-------------------------------------"""

    def getVipOrderNum(self, userId, biz_type):
        """
        通过手机号获取当前账户的会员购买列表
        :param biz_type:
        :param userId:
        :return:
        """
        """
        biz_type:
        1: B端会员 YUPAO_B_VIP
        2: C端会员 YUPAO_VIP
        3: 鱼泡次卡 YUPAO_SUB_CARD
        4: B端查看次卡 YUPAO_B_VISIT_CARD
        5: 竞招次卡组合 JOB_VIE_BUNDLE_CARD
        """
        data = {
            "bizType": biz_type,
            "userId": userId,
            "orderStatus": "PAY_SUCCESS",
            "refundStatus": "UN_REFUND"
        }
        self.headers.update({"Business": "mms"})
        url = self.hostname + r'/trade/v2/orderCenter/orderList'
        res = self.overRequest(url, data)
        # res = requests.post(url=url, json=data, headers=self.headers)
        infoList = res.json()['data']['data']
        if infoList:
            orderNoList = []
            for info in infoList:
                orderNoList.append([info['orderNo'], info['orderPrice'], info['id']])
            return orderNoList
        else:
            return None

    def vipOrderNoReturn(self, userId, biz_type):
        orderNoList = self.getVipOrderNum(userId, biz_type)
        msg = []
        if isinstance(orderNoList, list):
            for orderInfo in orderNoList:
                orderNo = orderInfo[0]
                orderPrice = orderInfo[1]
                orderId = orderInfo[2]
                data = {
                    "orderNo": orderNo,
                    "refundPrice": orderPrice,
                    "refundRemark": "自动化测试后置退积分",
                    "refundType": "ALL_REFUND",
                    "refundGoodsNum": "1",
                    "replay": "测试"
                }
                self.headers.update({"Business": "mms"})
                if biz_type == "YUPAO_VIP":
                    url = self.hostname + r'/trade/v2/refundCenter/refund'
                else:
                    url = self.hostname + r'/trade/v1/refund/order'
                res = self.overRequest(url, data)
                msg.append({orderNo: res.json()['message']})
                self.handlerRefundReview(msg, res, orderNo, orderId)
            return msg
        else:
            return {"code": 200, "msg": "当前账号未购买无需处理退费"}

    def callMyResume(self, userId):
        """
        :param userId:
        :return:
        """
        resumeUuid = self.getResumeUuid(userId)

        headers = {
            "env": "test"
        }
        url = "http://10.16.30.64:5001/resume/callMe"
        data = {
            "uuid": resumeUuid,
            "call_num": 1,
            "username": "luoshengwen"
        }
        res = self.sess.request(method='post', url=url, json=data, headers=headers)
        return res.json()

    """-------------------------------------用户查询-------------------------------------"""

    def getUserInfoByPhone(self, phone):
        """
        :param phone:
        :return:
        """
        url = self.hostname + r"/accountManage/v1/userQuery/queryByCondition"

        data = {
            "tel": phone,
            "tenantKey": "YPZP",
            "currentPage": 1,
            "pageSize": 10
        }

        res = self.overRequest(url, data)

        userId = res.json()["data"]["data"][0]["userId"]
        userIntegral = res.json()["data"]["data"][0]["integral"]

        return userId, userIntegral

    def getUserEnterpriseInfo(self, userId):
        """

        :param userId:
        :return:返回用户企业详情
        """
        url = self.hostname + r"/enterpriseManage/v2/masterData/pageQuery"
        data = {"currentPage": 1, "pageSize": 20, "userId": userId, "timeSelect": 1, "enterpriseStatus": 2}
        res = self.overRequest(url, data)
        print(res.json())

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
    def test(self,user_id):
        tel = self.getRealTelByHash(user_id)
        result = self.checkTelisallow(tel)
        if result == "true":
            print("手机号在测试白名单")
        else:
            print("手机号不在测试白名单")



if __name__ == '__main__':
    worker = WorkerMiddleControls()
    worker.test(25413713)



