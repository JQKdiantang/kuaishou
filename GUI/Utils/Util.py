# coding:utf-8
import ctypes
import datetime
import os
import re
import string
import sys
import psutil

from fake_useragent import FakeUserAgent

def rep_char(chars):
    """
    清洗文件名
    :param chars: 文件名称
    :return: chars
    """
    eg_punctuation = string.punctuation  # 英文标点符号
    ch_punctuation = string.punctuation  # 中文标点符号
    # print("所有标点符号：", eg_punctuation, ch_punctuation)

    for item1 in eg_punctuation:
        chars = chars.replace(item1, '')  # 将英文标点符号从字符串中移除

    for item2 in ch_punctuation:
        chars = chars.replace(item2, '')  # 将中文标点符号从字符串中移除

    chars = chars.replace(' ', '').replace('\n', '').replace('\xa0', '').replace('\r', '')  # 移除空格和换行符
    chars = chars.replace(':', '').replace('.', '').replace('*', '').replace('$', '')  # 移除冒号、句号、星号和美元符号
    chars = chars.replace('\t', '').replace('', '').replace('?', '').replace('%', '')  # 移除制表符、未知字符、问号和百分号
    chars = chars.replace('\\', '').replace('/', '').replace(':', '').replace('|', '')  # 移除反斜杠、斜杠、冒号和竖线
    chars = chars.replace('<', '').replace('>', '').replace('', '')  # 移除小于号、大于号和未知字符

    # 防止字符串过长导致文件创建失败
    if len(chars) > 100:
        chars = chars[0:50]

    return chars


def get_free_space():
    """
    磁盘剩余存储检查
    """
    folder = os.path.abspath(sys.path[0])
    if sys.platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 10


def GetInfo():
    link = 'https://www.kuaishou.com/graphql'
    # pcursor这个变量的值开始必须为空，不用动他，它是换页的参数
    pcursor = ''
    f = open("../Cookie", encoding="utf-8")
    ck = f.readline()
    ua = FakeUserAgent().random
    return link, pcursor, ck, ua


def GetUserAgent():
    return FakeUserAgent().random


def timestamp_to_datetime(timestamp):
    """
    将时间戳转换为日期时间格式

    参数:
        timestamp (int): 需要转换的时间戳

    返回值:
        datetime: 转换后的日期时间对象
    """
    timestamp = int(timestamp)
    timestamp = timestamp / 1000.0  # 将时间戳从毫秒转换为秒
    date_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return date_string


def contains_chinese(input_str):
    return bool(re.search(r'[\u4e00-\u9fa5]', input_str))


def get_disk_usage(path):
    """
    获取指定路径所在磁盘的使用情况
    """
    drive = os.path.splitdrive(path)
    # print(drive[0])
    disk_usage = psutil.disk_usage(drive[0])
    total_gb = round(disk_usage.total / (1024. ** 3), 2)
    used_gb = round(disk_usage.used / (1024. ** 3), 2)
    free_gb = round(disk_usage.free / (1024. ** 3), 2)
    usage_percentage = int(disk_usage.percent)
    # print(f"磁盘总大小：{total_gb} GB，已使用：{used_gb} GB，剩余：{free_gb} GB，磁盘使用率：{usage_percentage}%，磁盘路径：{path}")
    return total_gb, used_gb, free_gb, usage_percentage

