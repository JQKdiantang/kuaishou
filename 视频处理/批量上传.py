import os
import random
import subprocess
import sys
from time import sleep

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
    command = ['biliup.exe', 'upload', video_file, '--cover', cover_file, '--tag', tag, '--tid', tid]

    return_code = subprocess.call(command)

    # 检查返回码以了解命令执行情况
    if return_code == 0:
        print("命令执行成功")
    else:
        print(f"命令执行失败，返回码：{return_code}")
    return return_code


if __name__ == "__main__":
    directory = r"F:\直播复盘录制工具"
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
                #tag = '娱乐剪刀手安利大赛 '
                #tag = '新片新剧一起看 '
                #tag = '影视整活大赏 '

                tags = ['娱乐剪刀手安利大赛', '新片新剧一起看', '影视整活大赏']
                # 随机选取一个tag
                tag = random.choice(tags)
                tid = '183'
                # cover_file = '张软软-2024-02-24.jpg'
                return_code = upload_video_to_bilibili(video_file, tag, tid, cover_file)

                if return_code == 0:
                    success_count += 1
                    log_file.write(f"成功上传：{filename}\n")
                    log_file.flush()
                    sleep(1)
                    os.remove(cover_file)
                    os.remove(video_file)
                else:
                    failure_count += 1
                    log_file.write(f"上传失败：{filename}\n")
                    log_file.flush()
                    os.remove(cover_file)

    log_file.close()

    print(f"上传成功数量：{success_count}")
    print(f"上传失败数量：{failure_count}")
