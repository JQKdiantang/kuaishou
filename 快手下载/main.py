# coding:utf-8
import json
import string
import sys
import time
import ctypes
import os
import platform

from zhon.hanzi import punctuation

import requests
import urllib3
from 快手下载 import mySqlite

urllib3.disable_warnings()
from fake_useragent import FakeUserAgent


# 请求作品信息 H264
def req_data_h264(url, id, pcursor, ck, ua):
	# 请求头
	headers = {
		'content-type': 'application/json',
		'Cookie': ck,
		'Host': 'www.kuaishou.com',
		'Origin': 'https://www.kuaishou.com',
		'Referer': 'https://www.kuaishou.com/profile/' + id,
		'User-Agent': ua
	}
	# 请求参数
	data = {
		'operationName': 'visionProfilePhotoList',
		'query': "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: "
				 "String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: "
				 "$webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n  "
				 "      id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n "
				 "         url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        "
				 "type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n      "
				 "  caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n        "
				 "  cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n         "
				 " url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        "
				 "expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        "
				 "profileUserTopPhoto\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      "
				 "llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
		'variables': {'userId': id, 'pcursor': pcursor, 'page': 'profile'}
	}
	data = json.dumps(data)
	data_json = requests.post(url=url, headers=headers, data=data, timeout=26.05).json()
	# pprint.pprint(data_json)
	return data_json


# 请求作品信息 H265
def req_data_h265(url, id, pcursor, ck, ua):
	# 请求头
	headers = {
		'content-type': 'application/json',
		'Cookie': ck,
		'Host': 'www.kuaishou.com',
		'Origin': 'https://www.kuaishou.com',
		'Referer': 'https://www.kuaishou.com/profile/' + id,
		'User-Agent': ua
	}
	# 请求参数
	data = {
		'operationName': 'visionProfilePhotoList',
		'query': "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n "
				 " viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  "
				 "videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  "
				 "animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  "
				 "musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    "
				 "name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    "
				 "__typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  "
				 "status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  "
				 "__typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, "
				 "$webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, "
				 "webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      "
				 "...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
		'variables': {'userId': id, 'pcursor': pcursor, 'page': 'profile'}

	}
	data = json.dumps(data)
	data_json = requests.post(url=url, headers=headers, data=data, timeout=26.05).json()
	# pprint.pprint(data_json)
	return data_json


# 请求网页 作品数量
def req_data_num(url, id, ck, ua):
	# 请求头
	headers = {
		'content-type': 'application/json',
		'Cookie': ck,
		'Host': 'www.kuaishou.com',
		'Origin': 'https://www.kuaishou.com',
		'Referer': 'https://www.kuaishou.com/profile/' + id,
		'User-Agent': ua
	}
	# 请求参数
	data = {
		'operationName': 'visionProfile',
		'query': "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) "
				 "{\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        "
				 "fan\n        photo\n        follow\n        photo_public\n        __typename\n      }"
				 "\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n"
				 "        user_text\n        user_profile_bg_url\n        __typename\n      }\n      "
				 "isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n",
		'variables': {'userId': id}

	}
	data = json.dumps(data)
	data_json = requests.post(url=url, headers=headers, data=data, timeout=6.05).json()
	# pprint.pprint(data_json)
	return data_json


# 清洗文件名
def rep_char(chars):
	eg_punctuation = string.punctuation
	ch_punctuation = punctuation
	# print("所有标点符号：", eg_punctuation, ch_punctuation)
	for item1 in eg_punctuation:
		chars = chars.replace(item1, '')
	for item2 in ch_punctuation:
		chars = chars.replace(item2, '')
	chars = chars.replace(' ', '').replace('\n', '').replace('\xa0', '').replace('\r', '')
	chars = chars.replace(':', '').replace('.', '').replace('*', '').replace('$', '')
	chars = chars.replace('\t', '').replace('', '').replace('?', '').replace('%', '')
	chars = chars.replace('\\', '').replace('/', '').replace(':', '').replace('|', '')
	chars = chars.replace('<', '').replace('>', '').replace('', '')
	# 防止字符串过长 创建文件失败
	if len(chars) > 100:
		chars = chars[0:50]
	return chars


# 磁盘内存检查
def get_free_space():
	folder = os.path.abspath(sys.path[0])
	if platform.system() == 'Windows':
		free_bytes = ctypes.c_ulonglong(0)
		ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
		return free_bytes.value / 1024 / 1024 / 1024
	else:
		st = os.statvfs(folder)
		return st.f_bavail * st.f_frsize / 1024 / 10


# 保存数据
def save(url, page, ck, ua):
	try:
		TopFlag = 0
		except_lit = []
		count = 0
		is_new = True  # 是否有新作品标识
		idlist = get_ids()

		id_list_txt = idlist.copy()  # 用于更新txt文件的数组
		for id in idlist:
			works_time = "0"
			works_time = time1 = mySqlite.GetTimeDataForAuthor(id)  # 获取作品时间
			if time1 == "0" or time1 is None:  # 如果时间为0 需要重新从Download表重新获取
				works_time = time1 = mySqlite.GetTimeDataForDownload(id)
			if time1 is None:
				works_time = time1 = "0"

			# record = mySqlite.GetRecordData()  # 获取作品时间
			# for data in record:
			#     if id == data[0]:
			#         time1 = data[1]
			count = count + 1
			data = req_data_num(url, id, ck, ua)

			# 作品数量
			photo_public = data['data']['visionProfile']['userProfile']['ownerCount']['photo_public']
			# 作者名称
			author = data['data']['visionProfile']['userProfile']['profile']['user_name']
			author = rep_char(author)
			works_num = mySqlite.GetUserWorksNum(id);
			print(
				f'第{count}位关注：作者：{author} {id}  作品数：{photo_public}  存储作品数：{works_num} 存储时间： {works_time} 全部视频地址加载中...')
			num = 0
			# 循环下载视频，直到 page == 'no_more'
			while page != 'no_more':
				time.sleep(0.1)
				data = req_data_h265(url, id, page, ck, ua)
				# 获取翻页的参数
				next_page_Pcursor = data['data']['visionProfilePhotoList']['pcursor']
				page = next_page_Pcursor
				print(next_page_Pcursor)
				data_list = data['data']['visionProfilePhotoList']['feeds']
				for item in data_list:
					time.sleep(0.1)
					num = num + 1
					# 视频名称
					video_name = rep_char(item['photo']['caption'])

					# 视频地址 H265
					video_url = item['photo']['photoH265Url']
					if video_url is None or video_url == "":  # 如果没有H265 获取H264
						video_url = item['photo']['photoUrl']
					# 视频发布时间
					video_time = item['photo']['timestamp']
					# 作者名称
					author = rep_char(item['author']['name'])

					# 根据时间判断是否有新作品
					if int(video_time) <= int(time1):
						TopFlag+=1
						# 	防止置顶作品 时间干扰
						if TopFlag>3:
							is_new = False
							TopFlag=0
							break
						else:
							continue
					else:
						if int(works_time) < int(video_time):
							works_time = video_time

					# 保存视频地址
					datas = [id, video_time]
					if mySqlite.selectIsDownloadDate(datas) != 1:
						datas = [
							(id, video_url, video_time, video_name, False)
						]
						mySqlite.insertDownloadDate(datas)
					print(str(count) + "# " + str(photo_public) + "-" + str(num), author, video_name, video_time,
						  video_url)
					# print(f'作者：{author}  作品数：{photo_public}-{num}  作品名：{video_name} 作品时间： {video_time} 作品链接： {video_url} ')
				# 判断是否有新视频
				if not is_new:
					if works_time != '0':
						mySqlite.UpdateAuthorTime(id, works_time)
					works_time = '0'
					is_new = True
					break

			if works_time != '0':
				mySqlite.UpdateAuthorTime(id, works_time)
				print("更新最新作品时间", id, works_time)

			# pcursor = page 这个变量的值必须为空，不用动他，它是换页的参数
			page = ''
			print(f'第{count}位关注：{id} 全部视频地址加载完成！！！')

			# 移除当前完成的作者id
			id_list_txt.remove(id)
			# 重新写ID.txt
			with open("ID.txt", "w") as f:
				for item in id_list_txt:
					print(item, file=f, flush=True)
				f.close()

		# tasks = threadpool.makeRequests(func, authors)
		# [pool.putRequest(task) for task in tasks]
		# pool.wait()

	except:
		print("出错了:", id, works_time)
		# if works_time != '0':
		# 	mySqlite.UpdateAuthorTime(id, works_time)

	# finally:
		# if works_time != '0':
		# 	mySqlite.UpdateAuthorTime(id, works_time)
		# if len(id_list_txt)==0:
		# 	return
		# time.sleep(5)
		# save(link, pcursor, ck, ua)


# 获取全部关注页面数据
def req_follow_data(url, pcursor, ck, ua, selfid):
	# 请求头
	headers = {
		'content-type': 'application/json',
		'Cookie': ck,
		'Host': 'www.kuaishou.com',
		'Origin': 'https://www.kuaishou.com',
		'Referer': 'https://www.kuaishou.com/profile/' + selfid,
		'User-Agent': ua
	}
	# 请求参数
	data = {
		'operationName': 'visionProfileUserList',
		'query': 'query visionProfileUserList($pcursor: String, $ftype: Int) {\n  visionProfileUserList(pcursor: '
				 '$pcursor, ftype: $ftype) {\n    result\n    fols {\n      user_name\n      headurl\n      '
				 'user_text\n      isFollowing\n      user_id\n      __typename\n    }\n    hostName\n    pcursor\n   '
				 ' __typename\n  }\n}\n',
		'variables': {'ftype': 1, 'pcursor': pcursor}
	}
	data = json.dumps(data)
	follow_json = requests.post(url=url, headers=headers, data=data, timeout=7.05).json()
	# pprint.pprint(follow_json)
	return follow_json


# 获取全部喜欢数据
def req_follow_data_like(url, profile, pcursor, ck, ua, selfid):
	# 请求头
	headers = {
		'content-type': 'application/json',
		'Cookie': ck,
		'Host': 'www.kuaishou.com',
		'Origin': 'https://www.kuaishou.com',
		'Referer': 'https://www.kuaishou.com/profile/' + selfid,
		'User-Agent': ua
	}
	# 请求参数
	data = {
		'operationName': 'visionProfileLikePhotoList',
		'query': 'fragment photoContent on PhotoEntity  {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n'
				 'coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n'
				 '__typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n'
				 'profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n'
				 'id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n'
				 'photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n'
				 'type\n    name\n    __typename\n  }\n  __typename\n}\n\n'
				 'query visionProfileLikePhotoList($pcursor: String, $page: String, $webPageArea: String) '
				 '{\n  visionProfileLikePhotoList(pcursor: $pcursor, page: $page, webPageArea: $webPageArea)'
				 '{\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }'
				 ' \n    hostName\n    pcursor\n    __typename\n  }\n}\n',
		'variables': {'page': profile, 'pcursor': pcursor}
	}
	data = json.dumps(data)
	follow_json = requests.post(url=url, headers=headers, data=data, timeout=7.05).json()
	# pprint.pprint(follow_json)
	return follow_json


# 获取全部关注的id
def get_all_ids(url, page, ck, ua, selfid):
	id_list = []
	num = sign = 0
	fp = open('ID.txt', 'w')  # 打开文件
	# 循环保存id，直到 Pcursor == 'no_more'
	while page != 'no_more':
		# if len(id_list) > 1:
		#     return id_list
		time.sleep(0.2)
		follow_data = req_follow_data(url, page, ck, ua, selfid)
		# 获取翻页的参数
		next_pcursor = follow_data['data']['visionProfileUserList']['pcursor']
		page = next_pcursor
		print(page)
		sign = sign + 1
		print(f'第{sign}页:{next_pcursor}')
		fols_list = follow_data['data']['visionProfileUserList']['fols']
		time.sleep(0.1)
		for item in fols_list:
			num = num + 1
			user_name = item['user_name']
			user_name = rep_char(user_name)
			user_id = item['user_id']
			id_list.append(user_id)
			print(user_id, file=fp)
			# 将ID存储数据库
			datas = [user_id]
			if mySqlite.selectUserIdDate(datas) != 1:
				datas = [
					(user_id, user_name, "0")
				]
				mySqlite.insertAuthorDate(datas)

			print(f'{num}、 {user_name}：{user_id} >>> ID获取成功！！！')

	return id_list


# 获取全部喜欢的ID
def get_all_like(url, page, ck, ua, selfid):
	id_list = []
	num = sign = 0
	fp = open('ID.txt', 'w')  # 打开文件
	# 循环保存id，直到 Pcursor == 'no_more'
	while page != 'no_more':
		# if len(id_list) > 1:
		#     return id_list
		time.sleep(0.2)
		follow_data = req_follow_data_like(url, 'profile', page, ck, ua, selfid)
		# 获取翻页的参数
		next_pcursor = follow_data['data']['visionProfileLikePhotoList']['pcursor']
		page = next_pcursor
		print(page)
		sign = sign + 1
		print(f'第{sign}页:{next_pcursor}')
		fols_list = follow_data['data']['visionProfileLikePhotoList']['feeds']
		time.sleep(0.1)
		for item in fols_list:
			num = num + 1
			user_name = item['author']['name']
			user_name = rep_char(user_name)
			user_id = item['author']['id']
			id_list.append(user_id)
			print(user_id, file=fp)
			# 将ID存储数据库
			datas = [user_id]
			if mySqlite.selectUserIdDate(datas) != 1:
				datas = [
					(user_id, user_name, "0")
				]
				mySqlite.insertAuthorDate(datas)

			print(f'{num}、 {user_name}：{user_id} >>> ID获取成功！！！')

	return id_list


# 从文本中获取ID
def get_ids():
	id_list = []
	i = 0
	with open("ID.txt", "r") as f:  # 打开文件
		for data in f.readlines():
			data = data.strip('\n')
			id_list.append(data)
			i += 1
	print('ID获取成功 总数：', i)
	id_list = list(set(id_list))
	print('ID获取成功 去重后总数：',len(id_list))
	return id_list

def SetInfo():
	link = 'https://www.kuaishou.com/graphql'
	# pcursor这个变量的值开始必须为空，不用动他，它是换页的参数
	selfid = '3x45b8tsfd8kdsw'
	pcursor = ''
	f = open("Cookie", encoding ="utf-8")
	ck = f.readline()
	ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
	ua = FakeUserAgent().random
	print("'User-Agent':",ua)
	return link ,pcursor,ck,ua,selfid



path = 'D:/video'

if __name__ == '__main__':
	link,pcursor,ck,ua,selfid = SetInfo();
	# get_all_like(link, pcursor, ck, ua, selfid)  # 获取全部喜欢ID
	# get_all_ids(link, pcursor, ck, ua, selfid)  # 获取用户关注
	# mySqlite.FillAuthorData()  # 从数据库中获取ID

	save(link, pcursor, ck, ua)