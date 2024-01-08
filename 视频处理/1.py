import os

import cv2

video_path = r"D:\Download\抖音\暴走小雨好椅优选-2023-12-20 13-00-51.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print('无法打开视频文件')
ret, frame = cap.read()
if not ret:
    print('无法读取视频帧')
image_path = os.path.splitext(video_path)[0] + '.jpg'
print(image_path)
print(cv2.imwrite(image_path, frame))
cap.release()
