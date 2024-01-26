import glob
import hashlib
import os
import shutil
import struct
import subprocess
import re
import ffmpeg
from tqdm import tqdm
from moviepy.editor import *

import concurrent.futures


# 移动所有文件到根目录
def move_files(folder_path):
    """
     移动文件到指定目录
     :param folder_path: str, 文件路径
    """
    # 获取当前文件夹路径
    current_dir = folder_path

    # 遍历当前文件夹和子文件夹中的所有文件
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            # 构建文件路径
            file_path = os.path.join(root, file)

            # 新文件名
            new_file_name = file

            # 如果当前文件夹下已存在同名文件，则重命名文件
            counter = 1
            while os.path.exists(os.path.join(current_dir, new_file_name)):
                file_name, ext = os.path.splitext(file)
                new_file_name = "{}_{}{}".format(file_name, counter, ext)
                counter += 1

            # 移动文件到当前文件夹下
            shutil.move(file_path, os.path.join(current_dir, new_file_name))

    # 删除所有子文件夹
    for root, dirs, files in os.walk(current_dir, topdown=False):
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


def move_files_to_main_dir(main_dir):
    """
     移动文件到主目录
     :param main_dir: str, 文件路径
    """
    # 遍历主目录下的所有文件和文件夹
    for entry in os.listdir(main_dir):
        # 获取文件或文件夹的完整路径
        src_path = os.path.join(main_dir, entry)
        # 如果是文件，则将其移动到主目录中
        if os.path.isfile(src_path):
            dest_path = os.path.join(main_dir, entry)
            shutil.move(src_path, dest_path)
        # 如果是文件夹，则遍历文件夹下的所有文件和文件夹
        elif os.path.isdir(src_path):
            for sub_entry in os.listdir(src_path):
                sub_src_path = os.path.join(src_path, sub_entry)
                sub_dest_path = os.path.join(main_dir, sub_entry)
                # 将文件或文件夹移动到主目录中
                shutil.move(sub_src_path, sub_dest_path)
            # 删除原文件夹
            os.rmdir(src_path)


# 移动全部文件到根目录
def MoveFile():
    # 定义原始文件夹和目标文件夹的路径
    source_folder = r"D:\\360极速浏览器X下载\软件\B站"
    destination_folder = r"D:\\360极速浏览器X下载\软件\B站宅舞"

    # 遍历原始文件夹，包括子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".mp4"):
                # 构建源文件路径和目标文件路径
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)

                # 移动文件
                shutil.move(source_path, destination_path)


# 自定义比较函数，提取文件名中的数字部分并进行比较
def custom_compare(filename):
    # 使用正则表达式提取文件名中的数字部分
    number = int(re.search(r'\d+', filename).group())
    return number


# 自定义排序函数
def custom_sort(filenames):
    # 使用自定义的比较函数进行排序
    sorted_filenames = sorted(filenames, key=custom_compare)
    return sorted_filenames


def get_file_size(file_path):
    return os.path.getsize(file_path)


def sort_files_by_size(directory):
    files = os.listdir(directory)
    sorted_files = sorted(files, key=lambda x: get_file_size(os.path.join(directory, x)))
    return sorted_files


# 文件自动分组
def Classification(folder_path, group_size, flag):
    """
    文件自动分组
    :param folder_path: str, 路径
    :param group_size: int, 分组大小
    :param flag: bool, 是否启用自定义排序
    """
    if flag:
        # 获取所有文件名并按顺序排序
        # file_names = custom_sort(os.listdir(folder_path))
        file_names = sort_files_by_size(folder_path)
    else:
        file_names = os.listdir(folder_path)

    # 计算需要创建的文件夹数量
    num_folders = len(file_names) // group_size + (len(file_names) % group_size > 0)

    # 创建新文件夹
    for i in range(num_folders):
        folder_name = f'Folder {i + 1}'
        os.makedirs(os.path.join(folder_path, folder_name), exist_ok=True)

    # 移动文件到相应的文件夹中
    for i, file_name in enumerate(file_names):
        folder_index = i // group_size
        old_path = os.path.join(folder_path, file_name)
        new_folder = os.path.join(folder_path, f'Folder {folder_index + 1}')
        new_path = os.path.join(new_folder, file_name)
        os.rename(old_path, new_path)


# 自动排序并重命名 加序号
def rename_file(directory, flag, start_index=1):
    index = start_index
    # 遍历目录下所有文件和子目录
    for root, _, files in os.walk(directory):
        for file in files:
            # 获取子文件夹名字
            folder_name = os.path.basename(root)

            # 生成新文件名
            if flag:
                new_name = f"{index}-{folder_name}-{file}"
            else:
                new_name = f"{index}-{file}"

            # 构建旧路径和新路径
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_name)

            # 重命名文件
            os.rename(old_path, new_path)

            print(f"Renamed \"{file}\" to \"{new_name}\"")

            # 序号累加
            index += 1


##############################################################################

def is_video_file(file_name):
    try:
        # 使用VideoFile打开并检查文件是否为有效的视频文件
        video = VideoFileClip(file_name)
        video.close()
        return True
    except Exception as e:
        print(f"Skipping {file_name}: {str(e)}")
        return False


def convert_flv_to_mp4(input_file, output_file):
    # 硬件加速转化为h264格式视频 取决于显卡处理速度
    # command = f'ffmpeg  -hwaccel cuvid -c:v h264_cuvid -i "{input_file}" -c:v h264_nvenc -y "{output_file}" -y '

    # 直接拷贝视频流  同时处理音频为AAC 速度最快 取决于硬盘读写速度
    # command = f'ffmpeg -i "{input_file}" -c:v copy -c:a aac -strict experimental "{output_file}" -y '

    # 直接拷贝视频流
    command = f'ffmpeg -i "{input_file}" -c:v copy "{output_file}" -y'

    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(input_file)


def batch_convert_flv_to_mp4(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = [file_name for file_name in os.listdir(input_folder) if
                 file_name.endswith('.flv') or file_name.endswith('.mkv')]
    # 只添加视频文件
    # file_list = [file_name for file_name in os.listdir(input_folder) if is_video_file(os.path.join(input_folder, file_name)) ]

    # 主进程单线程工作
    for file_name in tqdm(file_list, desc='转换中', ncols=80):
        input_file = os.path.join(input_folder, file_name)
        # output_file = os.path.join(output_folder, file_name.replace('.flv', '.mp4'))
        output_file = os.path.join(output_folder, file_name[:file_name.rfind('.')] + '.mp4')
        # 如果输出文件不存在或者输入文件比输出文件新，则进行转换
        if not os.path.exists(output_file) or os.path.getsize(input_file) > os.path.getsize(output_file):
            convert_flv_to_mp4(input_file, output_file)

    # 主进程多线程工作
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     futures = [executor.submit(convert_flv_to_mp4, os.path.join(input_folder, file),os.path.join(output_folder, file[:file.rfind('.')] + '.mp4')) for file in file_list]
    #     for future in concurrent.futures.as_completed(futures):
    #         try:
    #             future.result()
    #         except Exception as exc:
    #             print(f'Caught exception in worker thread: {exc}')

    # 多进程多线程工作
    # with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
    #     futures = [executor.submit(convert_flv_to_mp4, os.path.join(input_folder, file),
    #                                os.path.join(output_folder, file[:file.rfind('.')] + '.mp4')) for file in file_list]
    #     for future in concurrent.futures.as_completed(futures):
    #         try:
    #             future.result()
    #         except Exception as exc:
    #             print(f'Caught exception in worker process: {exc}')


# 将FLV转换为MP4
def FLVToMP4(input_folder, output_folder):
    # 执行批量转换
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    batch_convert_flv_to_mp4(input_folder, output_folder)


##################################################################################
# 查找大于2GB的文件移动到指定目录
def move_large_videos(source_folder, target_folder):
    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            # 检查文件大小是否大于2GB
            if os.path.getsize(file_path) > 2 * 1024 * 1024 * 1024:
                # 移动文件到目标文件夹
                shutil.move(file_path, target_folder)
                print(f"Moved {file} to {target_folder}")


##################################################################################
def split_video(input_file, output_directory, num_segments):
    # 计算每个片段的时长
    # video_duration = get_video_duration(input_file)
    video_duration = get_video_duration2(input_file)
    segment_duration = video_duration / num_segments

    # 获取文件名称
    file_name = os.path.basename(input_file)
    file_name = file_name[:file_name.rfind('.')]
    # 使用FFmpeg执行切割命令
    for i in range(num_segments):
        start_time = i * segment_duration
        output_file = f"{output_directory}/{file_name}-{i + 1}.mp4"
        command = f"ffmpeg -i {input_file} -ss {start_time} -t {segment_duration} -r 25 -c:v copy -c:a copy  {output_file}"
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_video_duration(input_file):
    # 使用FFprobe获取视频时长
    command = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input_file}"
    output = subprocess.check_output(command, shell=True)
    duration = float(output)
    return duration


def get_video_duration2(input_file):
    # 使用FFprobe获取视频时长
    stream = ffmpeg.probe(input_file)
    duration = stream['format']['duration']
    return float(duration)


def get_duration(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            end = f.tell()
            f.seek(0)
            while f.tell() < end:
                if f.read(3) == b'web':
                    f.seek(14)
                    size = struct.unpack('>I', f.read(4))[0]
                    duration = struct.unpack('>I', f.read(4))[0] / 1000000.0
                    return duration
                f.seek(f.tell() + 1)
    except Exception:
        return None


# 切割文件
def SplitVideo(input_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for root, dirs, files in os.walk(input_file):
        for file in tqdm(files, desc='切割中', ncols=80):
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)

            if size > 2 * 1000 * 1024 * 1024:
                num_segments = round(size / (2 * 1000 * 1024 * 1024) + 0.5)

                # 如果不是.MP4 则先进行格式转换
                if not file_path.endswith('.mp4'):
                    output_file = os.path.join(root, file[:file.rfind('.')] + '.mp4')
                    convert_flv_to_mp4(file_path, output_file)
                    # 如果转换了格式 则更新文件名称
                    file_path = output_file
                split_video(file_path, output_directory, num_segments)
                os.remove(file_path)


##################################################################################

# 使用SHA256 删除重复文件
def delete_duplicate_files(folder_path):
    file_dict = {}
    # 遍历目标文件夹及其子文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    sha256_hash = hashlib.sha256(f.read()).hexdigest()
                    if sha256_hash in file_dict:
                        # 如果 SHA256 值已经存在，则删除当前文件
                        os.remove(file_path)
                        print(f'删除了：{file_path}')
                    else:
                        # 如果 SHA256 值不存在，则将当前文件的 SHA256 值添加到字典中
                        file_dict[sha256_hash] = file_name
                        print(sha256_hash, file_name)


##################################################################################

# 将文件夹中的文件 添加文件夹名字到文件名中
def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            parent_folder = os.path.basename(os.path.dirname(filepath))
            new_filename = f"{parent_folder}-{file}"
            new_filepath = os.path.join(root, new_filename)
            os.rename(filepath, new_filepath)
            print(f"Renamed: {file} -> {new_filename}")


#####################################################################################

# 删除文件名称中指定的字符串
def BatchRename():
    target_string = "download-"
    # target_string = "."
    # 遍历目标文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            # 如果文件名包含指定的字符串
            if target_string in name:
                # 获取文件名的前缀和后缀，删除指定字符串后拼接为新的文件名
                prefix = name[:name.index(target_string)]
                suffix = name[name.index(target_string) + len(target_string):]
                new_name = prefix + suffix

                # 重命名文件
                os.rename(os.path.join(root, name), os.path.join(root, new_name))


#####################################################################################

#####################################################################################
def group_files_into_subfolders(dir_path):
    file_size = 0;
    index = 1;
    # 遍历指定目录下的所有文件
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        # 如果是文件而不是文件夹
        if os.path.isfile(file_path):
            # 获取文件大小（以字节为单位）
            file_size1 = os.path.getsize(file_path)
            # 如果文件大小大于总大小，将其放入单独的文件夹中
            if file_size + file_size1 > 2 * 1000 * 1000 * 900:
                file_size = 0
                index += 1
                folder_name = dir_path + '/' + str(index)
                folder_path = os.path.join(dir_path, folder_name)
                # 如果文件夹不存在，则创建文件夹
                if not os.path.isdir(folder_path):
                    os.makedirs(folder_path)
                # 将文件移动到新文件夹中
                shutil.move(file_path, folder_path)
                print(f"Moved {filename} to {folder_name} because it's too large ({file_size} bytes)")
            else:
                file_size += file_size1
                default_folder_path = dir_path + '/' + str(index)
                # 如果文件夹不存在，则创建文件夹
                if not os.path.isdir(default_folder_path):
                    os.makedirs(default_folder_path)
                # 将文件移动到默认文件夹中
                shutil.move(file_path, default_folder_path)
                print(f"Moved {filename} to default folder because it's small ({file_size} bytes)")


# 删除文件名中指定文字
def replace_string_in_filename(directory, old_string, new_string):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        # 检查文件名是否包含旧字符串
        if old_string in filename:
            # 构建新的文件名
            new_filename = filename.replace(old_string, new_string)
            # 获取旧文件的完整路径
            old_file_path = os.path.join(directory, filename)
            # 获取新文件的完整路径
            new_file_path = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file_path, new_file_path)


#####################################################################################
# 按照大小分组
def group_files_into_subfolders(dir_path, max_size):
    file_size = 0
    index = 1
    # max_size = 2 * 1000 * 1000 * 900  # 2GB，以字节为单位
    # 遍历指定目录下的所有文件
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        # 如果是文件而不是文件夹
        if os.path.isfile(file_path):
            # 获取文件大小（以字节为单位）
            file_size1 = os.path.getsize(file_path)
            # 如果文件大小大于总大小，将其放入单独的文件夹中
            if file_size + file_size1 > max_size:
                file_size = 0
                index += 1
                folder_name = dir_path + '/' + str(index)
                folder_path = os.path.join(dir_path, folder_name)
                # 如果文件夹不存在，则创建文件夹
                if not os.path.isdir(folder_path):
                    os.makedirs(folder_path)
                # 将文件移动到新文件夹中
                shutil.move(file_path, folder_path)
                print(f"Moved {filename} to {folder_name} because it's too large ({file_size} bytes)")
            else:
                file_size += file_size1
                default_folder_path = dir_path + '/' + str(index)
                # 如果文件夹不存在，则创建文件夹
                if not os.path.isdir(default_folder_path):
                    os.makedirs(default_folder_path)
                # 将文件移动到默认文件夹中
                shutil.move(file_path, default_folder_path)
                print(f"Moved {filename} to default folder because it's small ({file_size} bytes)")


def delete_log_files(directory):
    # 在给定目录下查找.log文件
    for root, dirs, files in os.walk(directory):
        # Find .log files in the current directory (root)
        log_files = glob.glob(os.path.join(root, '*.log'))
        print(log_files)
        # 遍历找到的.log文件并删除
        for file in log_files:
            try:
                os.remove(file)
                print(f"文件 {file} 已被删除")
            except OSError as e:
                print(f"Error: {file} : {e.strerror}")


#####################################################################################

# 批量处理录制文件信息
def Process_files(directory):
    """
    批量处理录制文件信息
     :param directory: str, 文件路径
    """
    # 重命名添加主目录名称
    rename_files(directory)

    # 移动文件到主目录
    move_files(directory)

    # 删除文件名中指定文字
    replace_string_in_filename(directory, "已转码", "")

    # 删除.log文件
    delete_log_files(directory);


#####################################################################################


if __name__ == '__main__':
    # folder_path = r'D:\Download\软件\B站'
    # folder_path = r'D:\Download\软件\B站宅舞'
    # folder_path = r'D:\Download\软件\B站直播'
    # folder_path = r'D:\Download\软件\download'1
    # output_folder = r'D:\Download\软件\download1'

    folder_path = r'D:\直播复盘录制工具_N\抖音'
    # folder_path = r'E:\新建文件夹'
    # folder_path = r'E:\video'

    # 批量处理录制文件信息
    Process_files(folder_path)

    # 重命名添加主目录名称
    # rename_files(folder_path)

    # 移动文件到主目录
    # move_files(folder_path)

    # 删除文件名中指定文字
    # replace_string_in_filename(folder_path, "已转码", "")

    # 删除.log文件
    # delete_log_files(folder_path);

    # 分组视频
    # Classification(folder_path,600,True)

    # 转换格式
    # FLVToMP4(folder_path,folder_path)

    # 切割视频
    # SplitVideo(folder_path,folder_path)

    # 重命名添加序号
    # rename_file(folder_path,False,1)

    # 删除文件名称中指定的字符串
    # BatchRename()

    # 移动大于2 GB的文件
    # move_large_videos(folder_path,output_folder)
