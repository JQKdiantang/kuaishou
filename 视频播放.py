import cv2
import numpy as np
import os
import sys

# 设置视频缩放比例
scale = 0.2

# 设置视频文件路径
video_path = r"D:\Download\抖音\草莓蛋糕波波-2023-12-07 11-33-50.mp4"

# 获取视频文件的帧率
frame_rate = int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS))
delay = int(1000 / frame_rate)
# 创建VideoCapture对象来读取视频文件
cap = cv2.VideoCapture(video_path)

# 获取视频的原始宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 计算缩放后的宽度和高度
new_width = int(width * scale)
new_height = int(height * scale)

# 创建VideoWriter对象来写入处理后的视频文件
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 选择视频编码格式
# out = cv2.VideoWriter('output.mp4', fourcc, frame_rate, (new_width, new_height))


# 逐帧读取视频文件并进行处理
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # 如果读取失败，则退出循环
        break

        # 对帧进行缩放处理
    resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # 将处理后的帧写入输出视频文件
    # out.write(resized_frame)

    # 逐帧显示处理后的视频文件（可选）
    cv2.imshow('Scaled Video', resized_frame)
    if cv2.waitKey(delay) & 0xFF == ord('q'):  # 如果按下q键，则退出循环
        break

    # 释放资源并关闭窗口
cap.release()
# out.release()
cv2.destroyAllWindows()
