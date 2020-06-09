# -*- coding: utf-8 -*-
# @Time    : 2020-04-10 21:05
# @Author  : XU
# @File    : result_num.py
# @Software: PyCharm

success_count = {}
fail_count = {}


class Package_list():

    def su_append(self,result_package, target_channel, result_channel):
        global success_count
        success_count[result_package] = {
            "target_channel": target_channel,
            "result_channel": result_channel
        }

    def fa_append(self,result_package, target_channel, result_channel):
        global fail_count
        fail_count[result_package] = {
            "target_channel": target_channel,
            "result_channel": result_channel
        }