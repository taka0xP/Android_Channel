# -*- coding: utf-8 -*-
# @Time    : 2020-05-17 16:40
# @Author  : XU
# @File    : hw_cover.py
# @Software: PyCharm
from selenium.webdriver.common.by import By
from common.operation import Operation


def skip_hw_cover(driver):
    """首次安装华为市场包，关闭蒙层操作"""
    driver.find_element_by_id("com.tianyancha.skyeye:id/tab5").click()
    hw_company_detail = Operation(driver).isElementExist(By.ID, "com.tianyancha.skyeye:id/app_title_logo")
    if hw_company_detail:
        Operation(driver).back_up()
