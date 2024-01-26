import json

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
        'content-type': 'application/json',
        'Cookie': "kpf=PC_WEB; clientid=3; did=web_3321dd47bb93f9562c5e5b4be8e5fb3b; kpn=KUAISHOU_VISION",
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/search/author?searchKey=' + name,
        'User-Agent': ua
    }

    data={
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

def getAuthorPublicNum(user_id):
    url, pcursor,ck, ua = Util.GetInfo()
    data = req_data_num(url, user_id, ck, ua)
    # 作品数量
    photo_public = data['data']['visionProfile']['userProfile']['ownerCount']['photo_public']
    fan = data['data']['visionProfile']['userProfile']['ownerCount']['fan']
    follow = data['data']['visionProfile']['userProfile']['ownerCount']['follow']
    user_name = data['data']['visionProfile']['userProfile']['profile']['user_name']
    headurl = data['data']['visionProfile']['userProfile']['profile']['headurl']
    gender = data['data']['visionProfile']['userProfile']['profile']['gender']
    return fan,follow,photo_public, user_name,gender,headurl

def SearchUser(ksKey):
    url, pcursor, ck, ua = Util.GetInfo()
    data = req_data_Searchr(url, ksKey, ck, ua)
    # 作品数量
    name = data['data']['visionSearchPhoto']['feeds'][0]['author']['name']
    id = data['data']['visionSearchPhoto']['feeds'][0]['author']['id']
    return name, id

if __name__ == '__main__':
    SearchUser("3xrjqvg98t9xxi4")