# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 16:45
# @Author  : XU
# @File    : test_case.py
# @Software: PyCharm
from selenium.common.exceptions import TimeoutException

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from Providers.logger import Logger, error_format
from threading import Lock
from Providers.account.account import Account
import unittest
import warnings
from Providers.skip_guide import skip_guide, agree_license
from Providers.cancel_update import cancel_update
from Providers.statr_server import stater, stop_device, stop_server, uninstall_package
from element_Android import ele
from Providers import result_num

log = Logger("Android").getlog()


class TestChannel(unittest.TestCase, Operation):
    """Android「市场包」「渠道包」抽测脚本"""

    account = Account()
    package_list = result_num.Package_list()
    lock = Lock()

    def setUp(self):
        # 忽略waring提示
        warnings.simplefilter("ignore", ResourceWarning)
        self.driver, self.device, self.port, self.package = stater()
        agree_license(self.driver)
        skip_guide(self.driver)
        cancel_update(self.driver)
        self.phone_number = self.account.get_account("vip")

    def tearDown(self):
        # 回到首页
        self.driver.quit()
        # 加锁
        with self.lock:
            # 释放 设备 及 服务
            self.account.release_account(self.phone_number, "vip")
            uninstall_package(self.device)
            stop_device(self.device)
            stop_server(self.port)

    @getimage
    def test_channel(self):
        self.__result_channel = ''
        self.__target_channel = ''
        __package = self.package.split('/')[-1]
        self.__fail_detail = ''
        __retry = 7

        try:
            # 登录
            login_tag = 0
            while login_tag < __retry:
                try:
                    self.login(self.phone_number, self.account.get_pwd())
                    self.__fail_detail = ''
                except Exception as e:
                    login_tag += 1
                    self.back_up()
                    log.error(error_format(e) + "：包名「{}」".format(__package))
                    self.__fail_detail = '登录失败'
                    continue
                break

            # 查公司
            goal = "输入公司全称能搜索到公司"
            company_tag = 0
            company_name = ''
            while company_tag < __retry:
                try:
                    self.new_find_element(By.ID, ele.ELEMENT["首页搜索框"]).click()
                    self.new_find_element(By.ID, ele.ELEMENT["查公司—搜索页搜索框"]).send_keys("北京金堤科技有限公司")
                    company_name = self.new_find_element(By.XPATH, ele.ELEMENT["查公司—搜索结果页-Item1公司名"]).text
                    self.back_up()
                    self.__fail_detail = ''
                except Exception as e:
                    company_tag += 1
                    self.back_up()
                    log.error(error_format(e) + "：包名「{}」".format(__package))
                    self.__fail_detail = '查公司失败'
                    continue
                break
            self.assertEqual(company_name, "北京金堤科技有限公司", "错误————%s" % goal)

            # 查老板
            human_tag = 0
            human_list = True
            while human_tag < __retry:
                try:
                    self.new_find_element(By.ID, ele.ELEMENT["首页-查老板tab"]).click()
                    self.new_find_element(By.ID, ele.ELEMENT["首页搜索框"]).click()
                    self.new_find_element(By.ID, ele.ELEMENT["查老板-搜索页搜索框"]).send_keys("柳超")
                    human_list = self.isElementExist(By.XPATH, ele.ELEMENT['查老板-搜索结果页-无结果'])
                    self.back_up()
                    self.__fail_detail = ''
                except Exception as e:
                    human_tag = human_tag + 1
                    self.back_up()
                    log.error(error_format(e) + "：包名「{}」".format(__package))
                    self.__fail_detail = '查老板失败'
                    continue
                break
            self.assertFalse(human_list, "查老板搜索无结果")

            # 查关系
            relation_tag = 0
            relation_point = ''
            while relation_tag < __retry:
                try:
                    self.new_find_element(By.ID, ele.ELEMENT["首页-查关系tab"]).click()
                    self.new_find_element(By.XPATH, ele.ELEMENT["查关系热搜"]).click()
                    self.new_find_element(By.ID, ele.ELEMENT["关系图页-全屏按钮"]).click()
                    relation_point = self.new_find_element(By.XPATH, ele.ELEMENT["关系图节点"])
                    self.back_up()
                    self.__fail_detail = ''
                except Exception as e:
                    relation_tag += 1
                    self.back_up()
                    log.error(error_format(e) + "：包名「{}」".format(__package))
                    self.__fail_detail = '查关系失败'
                    continue
                break
            self.assertTrue(relation_point, "===失败-关系图全屏展示后，图谱节点展示异常===")

            # 登出
            logout_tag = 0
            while logout_tag < __retry:
                try:
                    self.logout()
                    self.__fail_detail = ''
                except Exception as e:
                    logout_tag += 1
                    self.back_up()
                    log.error(error_format(e) + "：包名「{}」".format(__package))
                    self.__fail_detail = '退出登录失败'
                    continue
                break

            # 渠道校验
            channel_tag = 0
            while channel_tag < __retry:
                try:
                    self.new_find_element(By.ID, ele.ELEMENT["首页我的"]).click()
                    self.swipeUp()
                    self.new_find_element(By.ID, ele.ELEMENT["联系我们"]).click()
                    for i in range(7):
                        self.new_find_element(By.ID, ele.ELEMENT["天眼查版本"]).click()
                    self.__result_channel = self.get_toast()
                    self.__target_channel = self.check_channel(__package.lower())
                    self.back_up()
                    self.__fail_detail = ''
                except Exception as e:
                    channel_tag += 1
                    self.back_up()
                    log.error(error_format(e) + "：渠道校验失败，包名「{}」".format(__package))
                    self.__fail_detail = '渠道校验失败'
                    continue
                break
            self.assertTrue(self.__result_channel == self.__target_channel,
                            '【失败】渠道名:{},包名:{}'.format(self.__result_channel, __package))

            # 更新配置校验
            update_tag = 0
            update_toast = ''
            while update_tag < __retry:
                try:
                    self.new_find_element(By.ID, ele.ELEMENT["首页我的"]).click()
                    self.swipeUp()
                    self.new_find_element(By.ID, ele.ELEMENT["版本更新"]).click()
                    try:
                        update_toast = self.get_toast()
                    except TimeoutException as e:
                        pass
                    if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_finish"):
                        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_finish").click()
                    else:
                        self.new_find_element(By.ID, "android:id/button1").click()
                    self.swipeDown()
                    self.__fail_detail = ''
                except Exception as e:
                    update_tag += 1
                    log.error(error_format(e) + "：更新配置校验失败，包名「{}」".format(__package))
                    self.__fail_detail = '更新配置校验失败'
                    continue
                break
            self.assertFalse(update_toast == '系统异常', "===点击更新「系统异常」===")

            log.info("【测试通过】--包名：{}".format(__package))
            self.package_list.su_append(__package, self.__target_channel, self.__result_channel)
        except Exception as e:
            log.info("【任务执行异常】--包名：{}".format(__package))
            if self.__target_channel == '':
                self.__target_channel = self.check_channel(__package)
                self.__result_channel = self.__fail_detail
            self.package_list.fa_append(__package, self.__target_channel, self.__result_channel)
            log.error(error_format(e))


if __name__ == "__main__":
    unittest.main()
