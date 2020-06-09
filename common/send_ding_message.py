# -*- coding: utf-8 -*-
# @Time    : 2020-03-05 10:24
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : send_ding_message.py
# @Software: PyCharm
import requests
import json


def send_message(content, pas, fail, error):
    ding_token = "https://oapi.dingtalk.com/robot/send?access_token=d1df0c97c37928eaaac174bb5d98dfbebbf044a771159b04d5d325a8785273c1"
    header = {"Content-Type": "application/json ;charset=utf-8 "}
    msg = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Android_Channel_Auto_Report",
            "text": "## Android「市场包」「渠道包」自动化结果：\n"
            + ">### 通过：{}\n".format(pas)
            + ">### 失败：{}\n".format(fail)
            + ">### 失败包名列表：{}\n".format(error)
            + "## [click me look more]({})".format(content),
        },
        "at": {"isAtAll": True},
    }
    send_msg = json.dumps(msg)
    requests.post(ding_token, data=send_msg, headers=header)


if __name__ == "__main__":
    send_message(
        "http://10.2.20.198:10001/app_auto_result/2020-03-05-085704/index.html",
        66,
        6,
        6,
    )
