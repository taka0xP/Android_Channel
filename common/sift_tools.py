# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 09:13
# @Author  : XU
# @File    : sift_tools.py
# @Software: PyCharm

from common.operation import Operation
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
import random
from selenium.webdriver.support.wait import WebDriverWait


class Tools(MyTest, Operation):
    def get_key(self, key, value, index, element):
        """
        获取高级筛选，选中项
        :param key: 高级筛选项，键集合
        :param value: 高级筛选项，值集合
        :param index: 选择项索引
        :return:返回被选中项key
        """
        listKey = element[key].split("###")
        listValue = element[value].split("###")
        origin = element[listKey[index - 1]]
        target = listValue[index - 1]
        if not self.isElementExist(By.ID, element["bt_reset"]):
            self.new_find_element(By.ID, element["select_more"]).click()
        # all = listKey.split("..")[0]
        all_icon = origin.split("..")[0] + "/following-sibling::android.widget.ImageView"
        for i in range(40):
            # if self.isElementExist(By.XPATH, origin):
            if self.isElementExist(By.XPATH, all_icon) or self.isElementExist(By.XPATH, origin):
                if self.isElementExist(By.XPATH, all_icon):
                    self.new_find_element(By.XPATH, all_icon).click();
                    break
                if target == self.new_find_element(By.XPATH, origin).text:
                    break
            else:
                l = self.driver.get_window_size()
                self.driver.swipe(
                    l["width"] * 0.5,
                    l["height"] * 0.55,
                    l["width"] * 0.5,
                    l["height"] * 0.15,
                    2000,
                )
            if i == 39:
                print("获取「" + target + "」失败")
        self.new_find_element(By.XPATH, origin).click()
        if self.isElementExist(By.ID, element["more_commit"]):
            self.new_find_element(By.ID, element["more_commit"]).click()
        elif self.isElementExist(By.XPATH, element["passwd_login"]):
            # 断言-未登陆态，拉起登陆页面
            self.assertEqual(
                element["passwd_login_text"],
                self.new_find_element(By.XPATH, element["passwd_login"]).text,
                "===失败-拉起登陆页失败===",
            )
            self.new_find_element(By.ID, element["title_back"]).click()
        elif self.isElementExist(By.ID, element["ll_go_pay"]):
            # 断言-非vip，拉起vip弹窗
            self.assertEqual(
                element["tv_middle_title_text"],
                self.new_find_element(By.ID, element["tv_middle_title"]).text,
                "===失败-弹出vip弹窗失败===",
            )
            self.driver.keyevent(4)

        return listKey[index - 1]

    def back2relation_search(self, inputTarget, element):
        """
        从公司详情页检验完成后，回到查关系
        :param inputTarget: 搜索关键词
        """
        for i in range(20):
            if self.isElementExist(By.ID, element["clear_all"]):
                self.new_find_element(By.ID, element["clear_all"]).click()
                self.new_find_element(By.ID, element["delete_confirm"]).click()
                self.new_find_element(By.ID, element["from_input_textview"]).click()
                self.new_find_element(By.ID, element["search_input_edit"]).send_keys(
                    inputTarget
                )
                break
            else:
                self.driver.keyevent(4)

    def back2company_search(self, element):
        """
        从公司详情页检验完成后，回到查公司
        """
        for i in range(20):
            if self.isElementExist(By.ID, element["search_sort_or_cancel"]):
                break
            else:
                self.driver.keyevent(4)

    def more_search_clear(self, targetSelect, element):
        """
        重置高级筛选项
        :param targetSelect: 被选中筛选项
        """

        if self.isElementExist(By.ID, element["bt_reset"]):
            if targetSelect is None:
                self.new_find_element(By.ID, element["bt_reset"]).click()
            else:
                self.new_find_element(By.XPATH, element[targetSelect]).click()
        else:
            if not self.isElementExist(By.ID, element["select_more"]):
                self.swipeDown()
            self.new_find_element(By.ID, element["select_more"]).click()
            if targetSelect is None:
                self.new_find_element(By.ID, element["bt_reset"]).click()
            else:
                self.new_find_element(By.XPATH, element[targetSelect]).click()

    def login_vip(self, element, phone_num_vip, phone_passwd):
        """
        登陆vip账号
        """
        if self.is_login():
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            if (
                "到期时间"
                in self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tv_user_type"
                ).text
            ):
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                ).click()
            else:
                self.logout()
                self.login(phone_num_vip, phone_passwd)
        else:
            self.login(phone_num_vip, phone_passwd)

    def login_normal(self, element, phone_num_normal, phone_passwd):
        """
        登陆普通账号
        """
        if self.is_login():
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            if (
                "到期时间"
                not in self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tv_user_type"
                ).text
            ):
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                ).click()
            else:
                self.logout()
            self.login(phone_num_normal, phone_passwd)
        else:
            self.login(phone_num_normal, phone_passwd)

    def send_target_key(self, tag, element, log):
        """
        输入搜索关键词
        :param tag: 1:查公司；2：查关系
        :return: 返回输入的关键词
        """
        if tag == 1:
            self.new_find_element(By.ID, element["search_company"]).click()
        else:
            self.new_find_element(By.ID, element["search_relation"]).click()
        self.new_find_element(By.ID, element["search_box"]).click()
        tarList = element["from_input_target"].split("###")
        inputTarget = tarList[random.randint(0, len(tarList) - 1)]
        if tag == 2:
            self.new_find_element(By.ID, element["from_input_textview"]).click()
        self.new_find_element(By.ID, element["search_input_edit"]).send_keys(
            inputTarget
        )
        log.info("搜索词：" + inputTarget)
        return inputTarget

    def point2company(self, selectTarget, element):
        """
        从关系节点介入公司详情页
        :param selectTarget: 选中条件
        :return: 输入内容
        """
        selectText = self.new_find_element(By.ID, element["tv_title"]).text
        if self.isElementExist(By.ID, element["more_empty_view"]):
            print(selectText)
            Tools.more_search_clear(self, selectTarget, element)
        else:
            self.new_find_element(By.XPATH, element["from_target_item_1"]).click()
            self.new_find_element(By.XPATH, element["sky_canvas"]).click()
        return selectText

    def click2company(self, selectText, selectTarget, element, log):
        """
        用于查公司-更多筛选，点击搜索列表页中item
        :param selectText: 更多筛选-筛选项
        :param selectTarget: 搜索关键词
        :param element: 元素数组
        :param log: 日志信息
        :return: 返回被校验公司名
        """
        if self.isElementExist(By.ID, element["more_empty_view"]):
            log.info("「" + selectText + "」筛选无结果")
            Tools.more_search_clear(self, selectTarget, element)
        else:  # 查公司-「机构类型」筛选
            items = Tools.random_swip_get_list(self, element)
            log.info("「" + selectText + "」，搜索结果页-公司列表长度：" + str(items))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_name_ele = self.new_find_element(
                By.XPATH,
                element["company_list"]
                + "["
                + str(items)
                + "]"
                + element["company_name_path"],
            )
            company_name = company_name_ele.text
            log.info("断言公司名称：" + company_name)
            company_name_ele.click()
        return company_name

    def random_swip_get_list(self, element):
        """
        搜索列表页，随机上滑
        :param element: 元素数组
        :return: 返回搜索列表页，list长度
        """
        l = self.driver.get_window_size()
        for i in range(random.randint(2, 6)):
            self.driver.swipe(
                l["width"] * 0.5,
                l["height"] * 0.8,
                l["width"] * 0.5,
                l["height"] * 0.3,
                1000,
            )
        return len(self.new_find_elements(By.XPATH, element["company_list"]))

    def get_company_baseinfo_4_relation(
        self, selectTarget, inputTarget, element, log, index=None
    ):
        """
        获取公司：基本信息(网址、邮箱)并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        selectText = Tools.point2company(self, selectTarget, element)
        company_name = self.new_find_element(By.ID, element["firm_detail_name_tv"]).text
        log.info("高级筛选：" + selectText + "，断言公司名称：" + company_name)
        if "邮箱" in selectText:
            if index == 1:  # 有邮箱
                self.assertEqual(
                    "true",
                    self.driver.find_element_by_id(
                        element["tv_base_info_email"]
                    ).get_attribute("enabled"),
                    "===失败-「" + selectText + "」，断言失败===",
                )
            else:  # 无邮箱
                if not self.isElementExist(
                    By.ID, "com.tianyancha.skyeye:id/iv_claim_label"
                ):
                    if "true" == self.driver.find_element_by_id(
                        element["tv_base_info_email"]
                    ).get_attribute("enabled"):
                        log.info("===公司被认证，企业主上传了「邮箱信息」===")
                else:
                    self.assertEqual(
                        "false",
                        self.driver.find_element_by_id(
                            element["tv_base_info_email"]
                        ).get_attribute("enabled"),
                        "===失败-「" + selectText + "」，断言失败===",
                    )
        else:
            if index == 1:  # 有网址
                self.assertEqual(
                    "true",
                    self.driver.find_element_by_id(
                        element["tv_base_info_web"]
                    ).get_attribute("enabled"),
                    "===失败-「" + selectText + "」，断言失败===",
                )
            else:  # 无网址
                if not self.isElementExist(
                    By.ID, "com.tianyancha.skyeye:id/iv_claim_label"
                ):
                    if "true" == self.driver.find_element_by_id(
                        element["tv_base_info_web"]
                    ).get_attribute("enabled"):
                        log.info("===公司被认证，企业主上传了「网址信息」===")
                else:
                    self.assertEqual(
                        "false",
                        self.driver.find_element_by_id(
                            element["tv_base_info_web"]
                        ).get_attribute("enabled"),
                        "===失败-「" + selectText + "」，断言失败===",
                    )
        Tools.back2relation_search(self, inputTarget, element)

    def get_company_detail_4_relation(
        self, detailText, selectTarget, inputTarget, element, log, index=None
    ):
        """
        获取公司：详情页维度
        :param detailText: 详情页维度名称
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """

        selectText = Tools.point2company(self, selectTarget, element)
        log.info(
            "高级筛选:"
            + selectText
            + "，断言公司名称："
            + self.new_find_element(By.ID, element["firm_detail_name_tv"]).text
        )
        for i in range(20):
            if self.isElementExist(
                By.XPATH,
                '//*[@class="android.widget.TextView" and @text="' + detailText + '"]',
            ):
                detailCount = self.isElementExist(
                    By.XPATH,
                    '//*[@class="android.widget.TextView" and @text="'
                    + detailText
                    + '"]/preceding-sibling::android.widget.TextView',
                )
                if detailText == "著作权":
                    if index == 2 and not detailCount:
                        # 断言-详情页「著作权」维度无数据时
                        self.assertFalse(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    else:
                        self.new_find_element(
                            By.XPATH,
                            '//*[@class="android.widget.TextView" and @text="'
                            + detailText
                            + '"]',
                        ).click()
                        targ = selectText[1:]  # 截取著作权类别
                        if targ == "软件著作权":
                            if index == 1:
                                self.assertNotIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["rjzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                            else:
                                self.assertIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["rjzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                        elif targ == "作品著作权":
                            if index == 1:
                                self.assertNotIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["zpzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                            else:
                                self.assertIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["zpzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                    break
                else:
                    if index == 1:
                        self.assertTrue(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    else:
                        self.assertFalse(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    break
            else:
                self.swipeUp(0.5, 0.7, 0.3, 2000)
                if i == 19:
                    log.info("断言失败-公司详情页未找到「" + detailText + "」")
        Tools.back2relation_search(self, inputTarget, element)

    def get_company_detail_4_company(
        self, detailText, selectTarget, element, log, index=None
    ):
        """
        获取公司：详情页维度
        :param detailText: 详情页维度名称
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """

        selectText = self.new_find_element(By.ID, element["tv_title"]).text
        Tools.click2company(self, selectText, selectTarget, element, log)
        for i in range(20):
            if self.isElementExist(
                By.XPATH,
                '//*[@class="android.widget.TextView" and @text="' + detailText + '"]',
            ):
                detailCount = self.isElementExist(
                    By.XPATH,
                    '//*[@class="android.widget.TextView" and @text="'
                    + detailText
                    + '"]/preceding-sibling::android.widget.TextView',
                )
                if detailText == "著作权":
                    if index == 2 and not detailCount:
                        # 断言-详情页「著作权」维度无数据时
                        self.assertFalse(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    else:
                        self.new_find_element(
                            By.XPATH,
                            '//*[@class="android.widget.TextView" and @text="'
                            + detailText
                            + '"]',
                        ).click()
                        targ = selectText[1:]  # 截取著作权类别
                        if targ == "软件著作权":
                            if index == 1:
                                self.assertNotIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["rjzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                            else:
                                self.assertIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["rjzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                        elif targ == "作品著作权":
                            if index == 1:
                                self.assertNotIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["zpzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                            else:
                                self.assertIn(
                                    "0",
                                    self.new_find_element(
                                        By.XPATH, element["zpzzq_detail_tab_layout"]
                                    ).text,
                                    "===失败-高级筛选：「" + selectText + "」错误===",
                                )
                    break
                else:
                    if index == 1:
                        self.assertTrue(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    else:
                        self.assertFalse(
                            detailCount, "===失败-高级筛选：「" + selectText + "」错误==="
                        )
                    break
            else:
                self.swipeUp(0.5, 0.7, 0.3, 2000)
                if i == 19:
                    log.info("断言失败-公司详情页未找到「" + detailText + "」")
        Tools.back2company_search(self, element)
        Tools.more_search_clear(self, selectTarget, element)

    def get_company_baseinfo_4_company(self, selectTarget, element, log, index=None):
        """
        获取公司：基本信息(网址、邮箱)并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """

        selectText = self.new_find_element(By.ID, element["tv_title"]).text
        Tools.click2company(self, selectText, selectTarget, element, log)
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element_by_id(element["tv_base_info_email"])
        )
        if "邮箱" in selectText:
            if index == 1:  # 有邮箱
                self.assertEqual(
                    "true",
                    self.driver.find_element_by_id(
                        element["tv_base_info_email"]
                    ).get_attribute("enabled"),
                    "===失败-「" + selectText + "」，断言失败===",
                )
            else:  # 无邮箱
                if not self.isElementExist(
                    By.ID, "com.tianyancha.skyeye:id/iv_claim_label"
                ):
                    if "true" == self.driver.find_element_by_id(
                        element["tv_base_info_email"]
                    ).get_attribute("enabled"):
                        log.info("===公司被认证，企业主上传了「邮箱信息」===")
                else:
                    self.assertEqual(
                        "false",
                        self.driver.find_element_by_id(
                            element["tv_base_info_email"]
                        ).get_attribute("enabled"),
                        "===失败-「" + selectText + "」，断言失败===",
                    )
        else:
            if index == 1:  # 有网址
                self.assertEqual(
                    "true",
                    self.driver.find_element_by_id(
                        element["tv_base_info_web"]
                    ).get_attribute("enabled"),
                    "===失败-「" + selectText + "」，断言失败===",
                )
            else:  # 无网址
                if not self.isElementExist(
                    By.ID, "com.tianyancha.skyeye:id/iv_claim_label"
                ):
                    if "true" == self.driver.find_element_by_id(
                        element["tv_base_info_web"]
                    ).get_attribute("enabled"):
                        log.info("===公司被认证，企业主上传了「网址信息」===")
                else:
                    self.assertEqual(
                        "false",
                        self.driver.find_element_by_id(
                            element["tv_base_info_web"]
                        ).get_attribute("enabled"),
                        "===失败-「" + selectText + "」，断言失败===",
                    )
        Tools.back2company_search(self, element)
        Tools.more_search_clear(self, selectTarget, element)

    def company_detail_into_company(self, element, log, company=None):
        if company is not None:
            self.new_find_element(By.ID, element["search_company"]).click()
            self.new_find_element(By.ID, element["search_box"]).click()
            self.new_find_element(By.ID, element["search_input_edit"]).send_keys(
                company
            )
            self.new_find_element(
                By.XPATH,
                '//*[@class="android.widget.TextView" and @text="' + company + '"]',
            ).click()
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element_by_id(element["tag_firm"])
            )
        else:
            Tools.send_target_key(self, 1, element, log)
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element_by_id(element["btn_export_data"])
            )
            items = Tools.random_swip_get_list(self, element)
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_item = self.new_find_element(
                By.XPATH,
                element["company_list"]
                + "["
                + str(items)
                + "]"
                + element["company_name_path"],
            )
            company_name = company_item.text
            log.info("断言公司名称：" + company_name)
            company_item.click()
            return company_name
