import os
import re


def remove_korean_chars(directory):
    index = 0
    # 正则表达式模式，匹配日文字符
    pattern = re.compile('[\u3040-\u309f\u30a0-\u30ff]')
    # 正则表达式模式，匹配韩文字符
    pattern = re.compile('[\uAC00-\uD7A3]')
    # r'[\uAC00-\uD7A3]'
    for filename in os.listdir(directory):
        if re.search(pattern, filename):  # 检测文件名中是否包含韩文字符
            new_filename = pattern.sub('', filename)  # 删除韩文字符
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))  # 重命名文件
            index += 1


# 调用函数，指定要处理的目录
remove_korean_chars("D:\新建文件夹")
