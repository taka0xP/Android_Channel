# -*- coding: utf-8 -*-
# @Time    : 2020-04-10 09:44
# @Author  : XU
# @File    : mount.py
# @Software: PyCharm
import os
import time

mount_com = 'mount -t cifs -o username="jindi",password="jindi" //10.2.20.127/share/ /Volumes/share/'


class Mount:
    def __init__(self):
        os.popen(mount_com)
        time.sleep(3)
