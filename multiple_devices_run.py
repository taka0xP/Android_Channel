# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-
# # # @Time    : 2019/11/28 17:05
# # # @Author  : Soner
# # # @version : 1.0.0

from threading import Thread, Lock
import unittest
import HTMLTestRunner_PY3
import time
import datetime
import os
from Providers.mount import Mount
from Providers.device_info import MachinePool
from Providers.package_info import ApkPool
from Providers.logger import Logger
from Providers.account.account import Account
from common.send_email import sendmail, result_item
from common.send_ding_message import send_message
from Providers.result_num import success_count, fail_count

log = Logger("main_program").getlog()
# 获取当前路径
now_dir = os.path.dirname(os.path.abspath(__file__))
# case路径
test_dir = now_dir + "/testcase"
# 报告路径
test_report = now_dir + "/report/HTML"
now = time.strftime("%Y-%m-%d-%H%M%S")
jenkins_path = "/opt/tomcat8/webapps/log/app_auto_result"


def kill_adb():
    os.popen("killall adb")
    os.popen("killall node")
    os.system("adb start-server")


def suit():
    global test_report
    testsuit = unittest.defaultTestLoader.discover(
        test_dir, pattern="test_case.py", top_level_dir=test_dir
    )
    if os.path.exists(jenkins_path):
        test_report = jenkins_path
    # 获取当前时间
    if not os.path.exists(test_report + "/{}".format(now)):
        os.makedirs(test_report + "/{}".format(now))

    # 定义测试报告的名字
    filename = test_report + "/{}_result.html".format(now)

    fp = open(filename, "wb")
    runner = HTMLTestRunner_PY3.HTMLTestRunner(
        stream=fp, title="APP 测试报告", description="运行环境Android"
    )
    runner.run(testsuit)
    fp.close()


def consumer(devices, lock):
    while True:
        with lock:
            status = devices.get_status()

        # 如果有可用设备
        if status:
            # 执行用例
            suit()
            # log.info(" {} 被我消费了".format(apk))
            break
        else:
            # 没有可用设备，则每隔10秒检测一次
            time.sleep(10)
            devices.change_device()


if __name__ == "__main__":
    start_time = time.time()
    s_time = datetime.datetime.now()
    log.info(time.strftime("开始时间：%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    kill_adb()

    lock = Lock()
    # 初始化账户列表
    Account().init_account()

    # 挂载 10.2.20.127
    Mount()

    # 获取APK文件列表
    apk_list = ApkPool()
    apk_list.init()

    # 设备操作 实例化
    devices = MachinePool()
    devices.init()

    threads = []

    # APK文件数，是否大于0
    while apk_list.update_apks() > 0:
        with lock:
            # 判断 是否有可用设备
            if not devices.get_status():
                time.sleep(2)
                continue
        try:
            thread = Thread(target=consumer, args=(devices, lock,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        except Exception as e:
            log.error(e)
        time.sleep(2)
        log.info("待安装APK数量：「{}」个".format(apk_list.update_apks()))

    for thread in threads:
        thread.join()

    index_url = "http://10.2.20.198:10001/app_auto_result/" + now + "/" + "index.html"
    end_time = time.time()
    e_time = datetime.datetime.now()
    log.info(time.strftime("开始时间：%Y-%m-%d %H:%M:%S", time.localtime(end_time)))

    try:
        fail_result = result_item(fail_count, "FAIL")
        succ_result = result_item(success_count, "SUCCESS")
        # send_message(index_url, len(success_count), len(fail_count), str(fails))
        sendmail(test_report + "/{}".format(now), s_time, e_time, len(success_count), len(fail_count), fail_result,
                 succ_result)
        log.info("send mail success")
    except Exception as e:
        log.error(e)
