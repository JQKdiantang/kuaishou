#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
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

        date = extract_date_time(filename)
        if date not in date_video_map:
            date_video_map[date] = []
        date_video_map[date].append(video_file)

    for date, video_list in date_video_map.items():
        output_file = f"{os.path.join(os.path.dirname(input_dir), output_prefix)}-{date}.mp4"

        input_list_file = 'list.txt'

        # 写入inputs.txt文件
        with open(input_list_file, 'w', encoding="utf-8") as f:
            for video in video_list:
                f.write(f"file '{video}'\n")
            # 在最后一行添加一个空行，这是ffmpeg concat滤镜要求的
            f.write("\n")

        # 定义ffmpeg合并命令
        concat_command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', input_list_file, '-c', 'copy', '-y',
                          output_file]

        # 执行ffmpeg命令
        subprocess.run(concat_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 删除临时文件（可选）
        os.remove(input_list_file)

        # 删除原始文件（请谨慎操作，确保合并成功后再删除）
        for original_video in video_list:
            os.remove(original_video)

def merge_videos2(input_dir, output_dir=None):
    """
    合并指定目录下相同文件名（或全部文件名相同）且同一天的所有视频，并在合并完毕后删除原始文件。
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

    date_filename_video_map = {}

    for video_file in files:
        # 解析视频文件名中的日期和时间以及基础文件名（不含日期）
        filename = os.path.basename(video_file)
        if '已转码' in filename:
            base_name = output_prefix
        else:
            base_name = extract_base_name(filename)  # 假设extract_base_name为提取无日期部分的函数
        date = extract_date_time(filename)

        if date not in date_filename_video_map:
            date_filename_video_map[date] = {}
        if base_name not in date_filename_video_map[date]:
            date_filename_video_map[date][base_name] = []
        date_filename_video_map[date][base_name].append(video_file)

    for date, filename_video_map in date_filename_video_map.items():
        for base_name, video_list in filename_video_map.items():
            if len(video_list) == 1:
                # 当相同名称的文件只有一个时，直接重命名并移动文件
                single_video = video_list[0]
                new_output_file = f"{os.path.join(os.path.dirname(input_dir), base_name)}-{date}.mp4"
                os.rename(single_video, new_output_file)
            else:
                output_file = f"{os.path.join(os.path.dirname(input_dir), base_name)}-{date}.mp4"
                input_list_file = 'list.txt'
                # 写入inputs.txt文件
                with open(input_list_file, 'w', encoding="utf-8") as f:
                    for video in video_list:
                        f.write(f"file '{video}'\n")
                    # 在最后一行添加一个空行，这是ffmpeg concat滤镜要求的
                    f.write("\n")

                # 定义ffmpeg合并命令
                concat_command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', input_list_file, '-c', 'copy', '-y',
                                  output_file]

                # 执行ffmpeg命令
                subprocess.run(concat_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # 删除临时文件（可选）
                os.remove(input_list_file)

                # 删除原始文件（请谨慎操作，确保合并成功后再删除）
                for original_video in video_list:
                    os.remove(original_video)


def extract_base_name(filename):
    # 假设日期和时间格式为 "基础名称-XXXX-XX-XX XX-XX-XX"
    pattern = r'^(.*)-\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}'

    match = re.match(pattern, filename)
    if match:
        return match.group(1)  # 返回基础文件名部分
    else:
        raise ValueError(f"无法从文件名 {filename} 中提取基础名称")


def extract_date_time(filename):
    # # 分别处理两种不同的文件命名格式
    # if '已转码' in filename:
    #     # 对于"已转码2024-02-05 20-35-32_xxxxx.mp4"这样的格式
    #     date_str = filename.split('已转码')[1].split(' ')[0]
    # else:
    #     # 对于"xxxxx-2024-01-31 08-11-37.mp4"这样的格式
    #     date_str, _ = filename.rsplit('.', 1)
    #     date_str = date_str.partition('-')[2]
    #     date_str = date_str.split(' ')[0]
    #
    # try:
    #     # 解析日期和时间
    #     date = datetime.strptime(date_str, '%Y-%m-%d')
    #     return date
    # except ValueError:
    #     # 如果无法解析日期，则返回None或抛出异常
    #     return None

    # 使用正则表达式匹配日期和时间
    date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})', filename)

    if date_match:
        date_str = date_match.group(1)
        try:
            # 解析日期和时间
            date = datetime.strptime(date_str, '%Y-%m-%d %H-%M-%S')
            return date.strftime('%Y-%m-%d')
        except ValueError:
            # 如果无法解析日期，则返回None
            return None
    else:
        return None


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
            os.rename(filepath, new_filepath)
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
    total_subdir = sum(1 for root, dirs, files in os.walk(directory) if files)
    pbar = tqdm(total=total_subdir)
    for root, dirs, files in os.walk(directory):
        merge_videos2(root, None)
        pbar.update(1)
    pbar.close()
    # 删除所有子文件夹
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            sub_dir = os.path.join(root, dir)
            if not os.listdir(sub_dir):  # 确保子目录为空
                os.rmdir(sub_dir)


if __name__ == "__main__":
    main_directory = r"D:\直播复盘录制工具_N\抖音"  # 主文件夹路径

    merge_videos_in_directory(main_directory)
    # main_directory = r"D:\新建文件夹"  # 主文件夹路径
    # merge_videos_in_directory(main_directory)
    # organize_files(main_directory)
