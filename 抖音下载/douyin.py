import csv
import json
import os
import time
from datetime import datetime

import requests


def read_csv_column(file_path, column_index):
    """
    读取CSV文件指定列数据到data中

    :param file_path: str, CSV文件路径
    :param column_index: int, 指定的列索引
    :return: list, 指定列的数据列表
    """
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > column_index:
                data.append(row[column_index])
    return data



if __name__ == '__main__':
    datas = read_csv_column(r"D:\Download\undefined.csv",0)
    num=0
    # 自动获取当前工作目录并生成文件名
    for data in datas:
        filepath = os.path.join(os.getcwd(), f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        video_content = requests.get(data, timeout=6.8).content
        with open(filepath, mode='wb') as f:
            f.write(video_content)
        time.sleep(1)
