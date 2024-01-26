from enum import Enum


class DownloadStatus(Enum):
    NOT_STARTED = 1 # 未开始，从未开始下载
    WAIT_FOR_DOWNLOAD = 2  # 等待下载，下载过，但是启动本次下载周期未开始，如重启程序后未开始
    PAUSE_STARTED = 3 # 暂停启动下载
    PAUSE = 4 # 暂停
    DOWNLOADING = 5# 下载中
    DOWNLOAD_SUCCEED = 6 #下载成功
    DOWNLOAD_FAILED = 7 # 下载失败
