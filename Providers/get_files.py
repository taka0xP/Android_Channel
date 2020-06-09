#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/7
# @Author  : Soner
# @version : 1.0.0

import os
from random import randint
from Providers.logger import Logger

log = Logger("case_files").getlog()


class CaseFilses:
    def __init__(self, file_name="test_", ex_name=".py"):
        """
        模糊查找文件
        :param now_dir:
        :param test_dir:
        :param file_name: 文件名匹配搜索的关键字
        :param ex_name: 文件的扩展名
        :return:
        """
        self.now_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_dir = self.now_dir + "/testcase/"

        # 获取指定路径下的所有文件，包括子目录
        files = list()
        for root, dirs, file in os.walk(test_dir):
            for f in file:
                if f.startswith(file_name) and f.endswith(ex_name):
                   files.append(f[:-3])
        self.case_files = []
        self.case_files = files
        # log.info("查找到的case文件列表：{}".format(self.case_files))

    def get_case_file(self):
        """
        随机获取一个文件
        """
        if self.case_files:
            count = len(self.case_files)
            random_num = randint(0, count - 1)
            case_file = self.case_files.pop(random_num)
            log.info("获取到用例文件：{}，并移除".format(case_file))
        else:
            case_file = None
            log.info("已经没有case文件")
        return case_file



if __name__ == "__main__":
    cases = CaseFilses()
    # for i in range(0, 1):
    #     cases.get_case_file()
    log.info(cases)
