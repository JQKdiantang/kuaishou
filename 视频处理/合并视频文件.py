#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import shutil
import subprocess
from datetime import datetime

from tqdm import tqdm


def merge_videos(input_dir, output_dir=None):
    """
    合并指定目录下同一天的所有视频文件，并在合并完毕后删除原始文件。
    输出文件将保存在与输入目录相同的目录中，文件名以前缀（即输入目录名）开头。

    参数：
        input_dir (str): 包含视频文件的目录路径。
        output_dir (str, optional): 输出目录，默认使用与input_dir相同的目录。
    """
    # 获取输入目录名作为输出前缀
    if output_dir is None:
        output_prefix = os.path.basename(os.path.normpath(input_dir))
    else:
        output_prefix = os.path.basename(output_dir)

    # 获取目录下的所有mp4文件
    files = glob.glob(os.path.join(input_dir, '*.mp4'))

    date_video_map = {}

    for video_file in files:
        # 解析视频文件名中的日期和时间
        filename = os.path.basename(video_file)
        try:
            date_str, _ = filename.split(' ', 1)  # 假设日期位于空格前的部分
            index= filename.index('-')
            date = datetime.strptime(date_str[index+1:], '%Y-%m-%d')  # 跳过'已转码'字样
            if date not in date_video_map:
                date_video_map[date] = []
            date_video_map[date].append(video_file)
        except ValueError:
            # 如果无法解析日期，则忽略该文件
            pass

    for date, video_list in date_video_map.items():
        output_file = f"{os.path.join(os.path.dirname(input_dir), output_prefix)}-{date.strftime('%Y-%m-%d')}.mp4"

        input_list_file = 'list.txt'

        # 写入inputs.txt文件
        with open(input_list_file, 'w', encoding="utf-8") as f:
            for video in video_list:
                f.write(f"file '{video}'\n")
            # 在最后一行添加一个空行，这是ffmpeg concat滤镜要求的
            f.write("\n")

        # 定义ffmpeg合并命令
        concat_command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', input_list_file, '-c', 'copy','-y', output_file]

        # 执行ffmpeg命令
        subprocess.run(concat_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 删除临时文件（可选）
        os.remove(input_list_file)

        # 删除原始文件（请谨慎操作，确保合并成功后再删除）
        for original_video in video_list:
            os.remove(original_video)


def delete_log_files(directory):
    # 在给定目录下查找.log文件
    for root, dirs, files in os.walk(directory):
        # Find .log files in the current directory (root)
        log_files = glob.glob(os.path.join(root, '*.log'))
        # 遍历找到的.log文件并删除
        for file in log_files:
            try:
                os.remove(file)
                print(f"文件 {file} 已被删除")
            except OSError as e:
                print(f"Error: {file} : {e.strerror}")


def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        print(dirs)
        files = os.listdir(root)
        for file in files:
            filepath = os.path.join(root, file)

            file.replace('已转码', '')
            parent_folder = os.path.basename(os.path.dirname(filepath))
            new_filename = f"{parent_folder}-{file}"
            new_filepath = os.path.join(root, new_filename)
            # os.rename(filepath, new_filepath)
            print(f"Renamed: {file} -> {new_filename}")

def organize_files(src_dir):
    """
    将源文件夹中的每个文件按照"-"前的名字创建相应文件夹并移动进去
    :param src_dir: 源文件夹路径
    """
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_dir):
        # 如果是文件（而不是目录）
        if os.path.isfile(os.path.join(src_dir, filename)):
            # 提取"-"之前的部分作为新的文件夹名称
            folder_name = filename.split('-')[0]
            subdir = os.path.join(src_dir, folder_name)
            os.makedirs(subdir, exist_ok=True)
            # 构建原文件完整路径
            old_file_path = os.path.join(src_dir, filename)
            # 构建新文件完整路径（即移动到新创建的子目录下）
            new_file_path = os.path.join(subdir, filename)
            # 移动文件
            shutil.move(old_file_path, new_file_path)
def merge_videos_in_directory(directory):
    delete_log_files(main_directory)
    total_subdirs = sum(1 for root, dirs, files in os.walk(directory) if files)
    pbar = tqdm(total=total_subdirs)
    for root, dirs, files in os.walk(directory):
        merge_videos(root, None)
        pbar.update(1)
    pbar.close()
    # 删除所有子文件夹
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            sub_dir = os.path.join(root, dir)
            if not os.listdir(sub_dir):  # 确保子目录为空
                os.rmdir(sub_dir)

if __name__ == "__main__":
    main_directory = r"F:\直播复盘录制工具\抖音"  # 主文件夹路径
    merge_videos_in_directory(main_directory)
    main_directory = r"G:\抖音"  # 主文件夹路径
    merge_videos_in_directory(main_directory)
    # organize_files(main_directory)
