# -*- coding: utf-8 -*-
# @Time    : 2019-10-14 09:39
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : send_email.py
# @Software: PyCharm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import zipfile
import os
import datetime
import time
from element_Android import ele

sender = 'xusirui@tianyancha.com'
password = 'X4aU69qBtYYRw8uK'
jenkins_param_emails = os.environ["emails"]
rec_list = jenkins_param_emails.split(';')
# rec_list = ['xusirui@tianyancha.com']
receivers = ','.join(rec_list)


def sendmail(report_path, start_time, end_time, pass_num, failed_num, fail_result, success_result):
    try:
        file_list = []
        for root, dirs, files in os.walk(report_path):
            for name in files:
                file_list.append(os.path.join(root, name))
        # 邮件内容
        msg = MIMEMultipart('mixed')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(["xusirui", sender])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = receivers
        # 邮件的主题
        msg['Subject'] = "Android_市场包/渠道包_测试总览"
        start = datetime.datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f')
        long = str(end_time - start_time)
        email_content = """
    <table class="tg" border="5" width="95%" cellpadding="10%" align="center">
        <th colspan="6">Android_V12.8.0_市场包/渠道包_测试总览</th>
        <tr>
            <td class="tg-pky" colspan="1" align="center">开始时间</td>
            <td class="tg-pky" colspan="2" align="center">{}</td>
            <td class="tg-pky" colspan="1" align="center">结束时间</td>
            <td class="tg-pky" colspan="2" align="center">{}</td>
        </tr>
        <tr>
            <td class="tg-pky" colspan="1" align="center">持续时间</td>
            <td class="tg-pky" colspan="2" align="center">{}</td>
            <td class="tg-pky" colspan="1" align="center">执行结果</td>
            <td class="tg-pky" colspan="2" align="center">通过：{} 失败：{}</td>
        </tr>
        <th colspan="6">Android_V12.8.0_市场包/渠道包_测试结果</th>
        <tr>
            <td class="tg-pky" colspan="3"  align="center">包名</td>
            <td class="tg-pky" colspan="1"  align="center">预期结果「渠道号」</td>
            <td class="tg-pky" colspan="1"  align="center">实际结果</td>
            <td class="tg-pky" colspan="1"  align="center">是否通过</td>
        </tr>
        {}
        {}
    </table>
            """.format(start, end, long, str(pass_num), str(failed_num), fail_result, success_result)
        texthtml = MIMEText(email_content, 'html', 'utf-8')
        # 将 alternative 加入 mixed 的内部
        msg.attach(texthtml)
        # SMTP服务器，腾讯企业邮箱端口是465，腾讯邮箱支持SSL(不强制)， 不支持TLS
        # qq邮箱smtp服务器地址:smtp.qq.com,端口号：456
        # 163邮箱smtp服务器地址：smtp.163.com，端口号：25
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        # 登录服务器，括号中对应的是发件人邮箱账号、邮箱密码
        server.login(sender, password)
        # 发送邮件，括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(sender, rec_list, msg.as_string())
        # 关闭连接
        server.quit()
    except Exception as msg:
        print(msg)


def result_item(count, result):

    channel_result = ''
    for channel_key in count.keys():
        package = channel_key
        target_channel = count[channel_key]["target_channel"].split('/')[-1]
        result_channel = count[channel_key]["result_channel"]
        if result == "SUCCESS":
            channel_result += ele.ELEMENT['报告结果条目'].format(package, target_channel, result_channel, "green", result)
        else:
            channel_result += ele.ELEMENT['报告结果条目'].format(package, target_channel, result_channel, "red", result)
    return channel_result


if __name__ == '__main__':
    a = datetime.datetime.now()
    time.sleep(3)
    b = datetime.datetime.now()
    fails = ''
    for i in range(10):
        fails = fails + '<p>' + str(i) + '</p>'
    sendmail('/Users/xu/Documents/workspace/android_channel/report/HTML/2020-02-21', a, b, 233, 4, fails)
