# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 18:19
# @Author  : XU
# @File    : package_info.py
# @Software: PyCharm


import os
from Providers.logger import Logger

log = Logger("package_info").getlog()



class ApkPool():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    apk_list = []

    def init(self):
        """查找apk文件"""
        jenkins_param_apk_path = os.environ["package_path"]
        # jenkins_param_apk_path = '/Users/xu/Downloads/test/'
        if jenkins_param_apk_path == "" or None:
            raise Exception("jenkins构建传参错误，请检查！！！！")
        # 获取指定路径下的所有文件，包括子目录
        for root, dirs, file in os.walk(jenkins_param_apk_path):
            for f in file:
                if f.endswith(".apk"):
                    self.apk_list.append(jenkins_param_apk_path + f)
        self.apk_list.sort()
        log.info("共{}个安装包".format(len(self.apk_list)))

    # 更新APK列表
    def update_apks(self):
        return len(self.apk_list)

    # 随机获取一个APK
    def get_apk(self):
        global apk_list
        if self.apk_list:
            apk_file = self.apk_list[0]
            self.apk_list.remove(apk_file)

            log.info("获取到APK文件：{}".format(apk_file))
        else:
            apk_file = None
            log.info("已经没有APK文件")
        return apk_file
