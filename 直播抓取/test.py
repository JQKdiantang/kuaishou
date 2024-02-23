from biliup.plugins.bili_webup import BiliBili, Data

video = Data()
video.title = '视频标题'
video.desc = '视频简介'
video.source = '添加转载地址说明'
# 设置视频分区,默认为160 生活分区
video.tid = 171
video.set_tag(['星际争霸2', '电子竞技'])
with BiliBili(video) as bili:
    bili.login_by_password("username", "password")
    for file in file_list:
        video_part = bili.upload_file(file)  # 上传视频
        video.append(video_part)  # 添加已经上传的视频
    video.cover = bili.cover_up('/cover_path').replace('http:', '')
    ret = bili.submit()  # 提交视频
