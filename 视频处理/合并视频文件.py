#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
import shutil
import subprocess
from datetime import datetime

import cv2
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


def merge_videos2(input_dir, output_dir=None, timestamp=None):
    """
    合并指定目录下相同文件名（或全部文件名相同）且同一天的所有视频，并在合并完毕后删除原始文件。
    输出文件将保存在与输入目录相同的目录中，文件名以前缀（即输入目录名）开头。

    参数：
        input_dir (str): 包含视频文件的目录路径。
        output_dir (str, optional): 输出目录，默认使用与input_dir相同的目录。
    """
    # 获取输出目录的实际路径
    if output_dir is None:
        output_base_dir = os.path.dirname(input_dir)
    else:
        output_base_dir = os.path.abspath(output_dir)
        # 如果输出目录不存在，则创建
        if not os.path.exists(output_base_dir):
            os.makedirs(output_base_dir)

    # 获取目录下的所有mp4文件
    files = glob.glob(os.path.join(input_dir, '*.mp4'))

    date_filename_video_map = {}

    for video_file in files:
        # 解析视频文件名中的日期和时间以及基础文件名（不含日期）
        filename = os.path.basename(video_file)
        if '已转码' in filename:
            # 获取输入目录名作为输出前缀
            base_name = os.path.basename(os.path.normpath(input_dir))
        else:
            base_name = extract_base_name(filename)  # 假设extract_base_name为提取无日期部分的函数
        date = extract_date_time(filename)
        # 当timestamp未提供或者拍摄日期早于给定时间时处理视频文件
        if timestamp is None or date < timestamp:
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
                new_output_file = f"{os.path.join(output_base_dir, base_name)}-{date}.mp4"
                # os.rename(single_video, new_output_file)
                shutil.move(single_video, new_output_file)
            else:
                output_file = f"{os.path.join(output_base_dir, base_name)}-{date}.mp4"
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
    # 匹配并提取时间戳及其两侧的部分
    pattern = r'(.*)[-_]?\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}([-_].*)'

    match = re.match(pattern, filename)

    if match:
        left_part = match.group(1).strip().replace('_', '').replace('-', '')
        right_part = match.group(2).strip().replace('_', '').replace('-', '') if match.group(2) else ''

        # 根据“_”的存在判断基础名称所在的位置
        if '_' in match.group():
            return right_part
        elif '-' in match.group(1):  # 新增：判断左侧是否包含破折号（-）
            return left_part

        # 如果左侧既没有下划线也没有破折号，则返回右侧部分
        return left_part if not right_part else right_part

    raise ValueError(f"无法从文件名 {filename} 中提取基础名称")


def extract_date_time(filename):
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


def delete_zero_size_files(directory):
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 查找.ts文件并检查其大小
        for file in files:
            if file.endswith('.ts'):
                file_path = os.path.join(root, file)
                # 获取文件大小
                size_in_bytes = os.path.getsize(file_path)

                # 如果文件大小为0字节，则尝试删除该文件
                if size_in_bytes == 0:
                    try:
                        os.remove(file_path)
                        print(f"文件 {file_path} 已被删除（大小为0KB）")
                    except OSError as e:
                        print(f"Error: {file_path} : {e.strerror}")


def convert_ts_to_mp4(input_dir, timestamp=None):
    delete_zero_size_files(input_dir)
    for root, dirs, files in tqdm(os.walk(input_dir), desc='总体进度'):
        for filename in files:
            if filename.endswith(".ts"):
                date = extract_date_time(filename)
                # 当timestamp未提供或者拍摄日期早于给定时间时处理视频文件
                if timestamp is None or date < timestamp:
                    input_file = os.path.join(root, filename)
                    base_name, ext = os.path.splitext(filename)
                    output_file = os.path.join(root, f"已转码{base_name}{'.mp4'}")

                    cmd = [
                        'ffmpeg',
                        '-i', input_file,  # 输入文件
                        '-c', 'copy', '-y',  # 使用copy命令，不重新编码
                        '-progress', '-',  # 将进度信息输出到标准错误流
                        output_file  # 输出文件
                    ]
                    # 执行ffmpeg命令
                    result = subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    # 检查转换是否成功
                    if result.returncode == 0:
                        os.remove(input_file)
                        print(f"{input_file} 已成功转换为 {output_file}")
                    else:
                        print(f"{input_file} 转换出错: {result.stderr}")


def convert_ts_to_mp42(input_dir, timestamp=None):
    delete_zero_size_files(input_dir)

    files_to_process = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".ts"):
                date = extract_date_time(filename)
                # 根据timestamp筛选需要处理的文件
                if timestamp is None or (timestamp and date < timestamp):
                    input_file = os.path.join(root, filename)
                    files_to_process.append((input_file, root))

    total_files = len(files_to_process)
    pbar = tqdm(total=total_files, desc='转换进度: ')

    for input_file, root in files_to_process:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        # output_file = os.path.join(output_dir, f"已转码{base_name}.mp4")
        output_file = os.path.join(root, f"已转码{base_name}{'.mp4'}")

        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c', 'copy', '-y',
            output_file
        ]

        try:
            pbar.set_description(f"当前处理的文件：{os.path.basename(input_file)} | 进度")
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"{os.path.basename(input_file)} 转换出错: {e.stderr.decode('utf-8')}")
        pbar.update(1)  # 更新进度条
        os.remove(input_file)
        continue
    pbar.close()


def check_timestamp_jumps(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("无法打开视频文件")
        return

    last_frame_ts = 0
    frame_count = 0
    max_jump_detected = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame_ts = cap.get(cv2.CAP_PROP_POS_MSEC)
        frame_count += 1

        # 计算时间戳差值（以毫秒为单位）
        timestamp_diff = current_frame_ts - last_frame_ts
        # 转换为帧数的预期差值
        expected_diff_frames = timestamp_diff / (1000 / fps)

        # 检查是否出现大于一帧以上的时间跳跃
        jump_frames = abs(expected_diff_frames - 1)
        if jump_frames > 1:
            max_jump_detected = max(max_jump_detected, jump_frames)
            print(f"在第 {frame_count} 帧发现时间戳跳变：{jump_frames:.2f} 帧")

        last_frame_ts = current_frame_ts

    cap.release()

    if max_jump_detected > 0:
        print(f"视频中检测到最大时间戳跳变为：{max_jump_detected:.2f} 帧")
    else:
        print("视频时间戳连续，未检测到明显跳变")


def check_audio_video_sync(input_video, verbose=False):
    """
    检查输入视频文件中的音频和视频是否同步。

    :param input_video: 输入视频文件路径。
    :param verbose: 是否详细打印时间戳信息，默认为False。
    """

    ffmpeg_command = f'ffprobe -i "{input_video}" -show_packets'
    result = subprocess.run(ffmpeg_command, shell=True, capture_output=True)

    # 解析ffprobe的输出结果，寻找音频和视频的时间戳
    audio_pts_list = []
    video_pts_list = []

    for line in result.stdout.decode('utf-8').splitlines():
        if "codec_type=audio" in line:
            packet_info = line.split(',')
            try:
                audio_pts = float(packet_info[packet_info.index("pts_time=") + 1])
                audio_pts_list.append(audio_pts)
            except ValueError:
                pass

        elif "codec_type=video" in line:
            packet_info = line.split(',')
            try:
                video_pts = float(packet_info[packet_info.index("pts_time=") + 1])
                video_pts_list.append(video_pts)
            except ValueError:
                pass

    # 简单的比较音频和视频的PTS差异
    if len(audio_pts_list) > 0 and len(video_pts_list) > 0:
        avg_audio_diff = sum([abs(a - b) for a, b in zip(audio_pts_list[:-1], audio_pts_list[1:])]) / (
                    len(audio_pts_list) - 1)
        avg_video_diff = sum([abs(v - w) for v, w in zip(video_pts_list[:-1], video_pts_list[1:])]) / (
                    len(video_pts_list) - 1)

        if verbose:
            print(f"音频平均时间戳差值: {avg_audio_diff:.2f} 秒")
            print(f"视频平均时间戳差值: {avg_video_diff:.2f} 秒")

        # 这里只是一个非常基础的判断，实际同步问题可能需要更复杂的逻辑分析
        if abs(avg_audio_diff - avg_video_diff) > 0.5:
            print("警告：可能存在音视频同步问题，请进一步分析.")
        else:
            print("初步检查未发现明显的音视频同步问题.")

    else:
        print("无法从视频中提取到有效的音频或视频时间戳信息.")


def fix_timestamp_jumps(input_video, output_video):
    """
    使用FFmpeg修复视频文件中的时间戳跳变问题。

    :param input_video: 输入视频文件路径。
    :param output_video: 修复后输出的视频文件路径。
    """

    # 构造FFmpeg命令
    ffmpeg_command = f'ffmpeg -i "{input_video}" -c copy -avoid_negative_ts make_zero -fflags +genpts "{output_video}"'

    try:
        # 执行FFmpeg命令
        subprocess.run(ffmpeg_command, shell=True, check=True)
        print(f"成功修复视频，输出至 {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"修复过程中发生错误: {e.stderr.decode('utf-8')}")


def fix_timestamp_jumps_and_sync(input_video, output_video):
    """
    使用FFmpeg修复视频文件中的时间戳跳变问题，并尝试同步音视频。

    :param input_video: 输入视频文件路径。
    :param output_video: 修复并同步后输出的视频文件路径。
    """

    # 构造FFmpeg命令，同时进行时间戳修正和音视频同步
    ffmpeg_command = f'ffmpeg -i "{input_video}" -c:v copy -c:a copy -map 0:v:0 -map 0:a:0 -async 1 -vsync 2 -avoid_negative_ts make_zero -fflags +genpts "{output_video}"'

    try:
        # 执行FFmpeg命令
        subprocess.run(ffmpeg_command, shell=True, check=True)
        print(f"成功修复并同步视频，输出至 {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"修复或同步过程中发生错误: {e.stderr.decode('utf-8')}")

    # `-async 1` 参数尝试对音频进行微调以实现与视频同步
    # `-vsync 2` 参数处理帧间的时间戳，通过重复或丢弃帧来适应视频流的时间基准


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


def merge_videos_in_directory(directory, output_dir=None, timestamp=None):
    delete_log_files(main_directory)
    delete_zero_size_files(main_directory)
    total_subdir = sum(1 for root, dirs, files in os.walk(directory) if files)
    pbar = tqdm(total=total_subdir, desc='处理进度: ')

    for root, dirs, files in os.walk(directory):
        # current_progress = pbar.n / total_subdir * 100
        pbar.set_description(f"当前处理的文件夹：{root} | 进度")
        merge_videos2(root, output_dir, timestamp)
        pbar.update(1)

    pbar.close()
    # 删除所有子文件夹
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            sub_dir = os.path.join(root, dir)
            if not os.listdir(sub_dir):  # 确保子目录为空
                os.rmdir(sub_dir)


if __name__ == "__main__":
    main_directory = r"G:\直播复盘录制工具/抖音"  # 主文件夹路径
    output_dir = r"F:\直播复盘录制工具"  # 主文件夹路径

    # 使用示例
    # check_audio_video_sync(r"D:\BDF2018.mp4", verbose=True)

    convert_ts_to_mp42("F:\抖音", '2024-02-28')

    # merge_videos_in_directory(main_directory, output_dir,'2024-02-27')
    # main_directory = r"D:\新建文件夹"  # 主文件夹路径
    # merge_videos_in_directory(main_directory)
    # organize_files(main_directory)
