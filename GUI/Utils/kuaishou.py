import json
import urllib.parse
import requests

from GUI.Utils import Util


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

    return data_json


# 请求作品信息
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

    # 2023-12-14更新
    data = {
        'operationName': 'visionProfilePhotoList',
        'query': "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  "
                 "viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n "
                 " videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  "
                 "animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n "
                 " musicBlocked\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  "
                 "caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  "
                 "photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  "
                 "timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n"
                 "  musicBlocked\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n "
                 "   headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n"
                 "    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n "
                 " __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n "
                 " visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n "
                 "   webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
        'variables': {'userId': id, 'pcursor': pcursor, 'page': 'profile'}
    }

    data = json.dumps(data)
    data_json = requests.post(url=url, headers=headers, data=data, timeout=26.05).json()
    return data_json


# 搜索用户
def req_data_Searchr(url, name, ck, ua):
    # 请求头
    headers = {
        'Content - Length': '1842',
        'content-type': 'application/json',
        'Cookie': "kpf=PC_WEB; clientid=3; did=web_950d56d7d66a6cc32bec3910ec6edea4; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; clientid=3; did=web_950d56d7d66a6cc32bec3910ec6edea4; client_key=65890b29; kpn=GAME_ZONE",
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/search/author?searchKey=' + name,
        'User-Agent': ua
    }
    data = {
        "operationName": "visionSearchPhoto", "variables": {"keyword": name, "pcursor": "", "page": "search"},
        "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption"
                 "\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url"
                 "\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp"
                 "\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto"
                 "\n  musicBlocked\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id"
                 "\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount"
                 "\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {"
                 "\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio"
                 "\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n}\n\nfragment feedContent on Feed {"
                 "\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename"
                 "\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }"
                 "\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }"
                 "\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {"
                 "\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {"
                 "\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor"
                 "\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    data = json.dumps(data)
    data_json = requests.post(url=url, headers=headers, data=data, timeout=26.05).json()
    return data_json


def req_data_Searchr2(url, name, ck, ua):
    # 请求头
    headers = {
        'content-type': 'application/json',
        'Cookie': "kpf=PC_WEB; clientid=3; did=web_950d56d7d66a6cc32bec3910ec6edea4; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; clientid=3; did=web_950d56d7d66a6cc32bec3910ec6edea4; client_key=65890b29; kpn=GAME_ZONE",
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/search/video?searchKey=' + name,
        'User-Agent': ua
    }
    print(headers['Referer'])
    data = {
        "operationName": "graphqlSearchUser", "variables": {"keyword": name},
        "query": "query graphqlSearchUser($keyword: String, $pcursor: String, $searchSessionId: String) {"
                 "\n  visionSearchUser(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId) {"
                 "\n    result\n    users {\n      fansCount\n      photoCount\n      isFollowing\n      user_id\n      headurl"
                 "\n      user_text\n      user_name\n      verified\n      verifiedDetail {\n        description\n        iconType"
                 "\n        newVerified\n        musicCompany\n        type\n        __typename\n      }\n      __typename\n    }"
                 "\n    searchSessionId\n    pcursor\n    __typename\n  }\n}\n"}
    data = json.dumps(data)
    data_json = requests.post(url=url, headers=headers, data=data, timeout=26.05).json()
    return data_json


def getAuthorPublicNum(user_id):
    url, pcursor, ck, ua = Util.GetInfo()
    data = req_data_num(url, user_id, ck, ua)
    # 作品数量
    photo_public = data['data']['visionProfile']['userProfile']['ownerCount']['photo_public']
    fan = data['data']['visionProfile']['userProfile']['ownerCount']['fan']
    follow = data['data']['visionProfile']['userProfile']['ownerCount']['follow']
    user_name = data['data']['visionProfile']['userProfile']['profile']['user_name']
    headurl = data['data']['visionProfile']['userProfile']['profile']['headurl']
    gender = data['data']['visionProfile']['userProfile']['profile']['gender']
    return fan, follow, photo_public, user_name, gender, headurl


def SearchUser(ksKey):
    if Util.contains_chinese(ksKey):
        ksKey = urllib.parse.quote(ksKey)

    url, pcursor, ck, ua = Util.GetInfo()
    data = req_data_Searchr2(url, ksKey, ck, ua)
    # 作品数量
    # name = data['data']['visionSearchPhoto']['feeds'][0]['author']['name']
    # id = data['data']['visionSearchPhoto']['feeds'][0]['author']['id']

    name = data['data']['visionSearchUser']['users'][0]['user_name']
    id = data['data']['visionSearchUser']['users'][0]['user_id']
    print(name, id)
    return name, id


if __name__ == '__main__':
    SearchUser("大表姐")
    # # 发送GET请求
    # response = requests.post('https://www.kuaishou.com')
    #
    # # 获取响应中的Cookie字典
    # cookies = response.cookies
    #
    # # 遍历Cookie字典，查找'did'键的值
    # did_value = None
    # for cookie_name, cookie_value in cookies.items():
    #     if cookie_name == 'did':
    #         did_value = cookie_value
    #         break
    #
    #         # 打印'did'的值
    # if did_value:
    #     print('did:', did_value)
    # else:
    #     print('Did not find the "did" cookie')
