import os
import subprocess
import sys

from tqdm import tqdm

from 视频处理.将视频转成图片 import get_first_frame


def upload_video_to_bilibili(video_file, tag, tid, cover_file):
    """
    封装上传视频到Bilibili的函数

    参数：
    video_file (str)：视频文件名
    tag (str)：视频标签
    tid (str)：视频分类ID
    cover_file (str)：封面图片文件名

    返回：
    result (subprocess.CompletedProcess)：执行命令后的结果对象，包含返回码和输出信息
    """

    # 构建命令参数列表
    command = ['biliup.exe', 'upload', video_file,  '--cover', cover_file ,'--tag', tag, '--tid', tid]

    return_code = subprocess.call(command)

    # 检查返回码以了解命令执行情况
    if return_code == 0:
        print("命令执行成功")
    else:
        print(f"命令执行失败，返回码：{return_code}")
    return return_code


if __name__ == "__main__":
    directory =r"D:\新建文件夹 (2)"
    success_count = 0
    failure_count = 0
    with open('upload_log.txt', 'w') as log_file:
        for filename in os.listdir(directory):
            if filename.endswith('.mp4'):  # 检查文件是否为视频文件
                video_file = os.path.join(directory, filename)
                image_path = get_first_frame(video_file)
                cover_file = image_path

                # 调用封装函数
                # video_file = '张软软-2024-02-24.mp4'
                tag = '影视神仙剪刀手'
                tid = '183'
                # cover_file = '张软软-2024-02-24.jpg'
                return_code = upload_video_to_bilibili(video_file, tag, tid, cover_file)

                if return_code == 0:
                    success_count += 1
                    log_file.write(f"成功上传：{filename}\n")
                    os.remove(video_file)
                    os.remove(cover_file)
                else:
                    failure_count += 1
                    log_file.write(f"上传失败：{filename}\n")
                    os.remove(cover_file)

    log_file.close()

    print(f"上传成功数量：{success_count}")
    print(f"上传失败数量：{failure_count}")

