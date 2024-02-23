import os
import sqlite3

import requests
import threadpool

from 快手下载 import main2


def create_database():
    if not os.path.exists('Download.db'):
        conn = sqlite3.connect('Download.db')
        with conn:
            conn.execute('''
            CREATE TABLE Download (
            user_id TEXT,
            url TEXT,
            time TEXT,
            isDownload blob,
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT);
            ''')
            conn.execute('''
                CREATE TABLE author (
                user_id TEXT,
                author TEXT,
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT); 
                ''')


def insertAuthorDate(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'insert into author (user_id, author,time) values(?, ?,?)'
    with conn:
        conn.executemany(sql, datas)
    conn.close()


def insertDownloadDate(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'insert into Download (user_id, url, time,video_name,isDownload) values( ?, ?, ?,?,?)'
    with conn:
        conn.executemany(sql, datas)
    conn.close()


def GetDownloadDate():
    authors = []
    conn = sqlite3.connect('Download.db')
    # conn.row_factory = sqlite3.Row
    sql = 'select d.user_id,d.url,d.time,d.isDownload,d.video_name,d.id,a.author from Download d inner join author a on d.user_id=a.user_id WHERE d.isDownload=0'
    # sql = 'select user_id,url,time,isDownload,video_name,id, user_id from Download WHERE isDownload=0'

    with conn:
        datas = conn.execute(sql, )
        for data in datas:
            video = [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]
            # print(data[0], data[1], data[2], data[3])
            videos = (video, None)
            authors.append(videos)
        return authors


def GetAuthor():
    id_list = []
    conn = sqlite3.connect('Download.db')
    sql = 'SELECT  user_id FROM author;'
    with conn:
        datas = conn.execute(sql, )
        for data in datas:
            id_list.append(data[0])
        return id_list


def UpdateDate(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'Update  Download set  isDownload = ? where url = ? '
    with conn:
        conn.executemany(sql, datas)
    conn.close()


def UpdateDates(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'Update  Download set  isDownload = 1 where url = ? '
    cursor = conn.cursor()
    # with conn:
    cursor.executemany(sql, datas)
    cursor.close()
    conn.commit()
    conn.close()


# 高效率
def UpdateDates2(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'REPLACE INTO Download (user_id,url,time,isDownload,video_name,id) values(?,?,?,?,?,?) '
    cursor = conn.cursor()
    # with conn:
    cursor.executemany(sql, datas)
    cursor.close()
    conn.commit()
    conn.close()


def xxxxxxx():
    conn = sqlite3.connect('Download.db')
    sql = 'select * from Download '
    with conn:
        datas = conn.execute(sql, )
        for url in datas:
            da = (url[0], '', url[2], True, '', url[5])
            DownloadData.append(da)
    conn.close()
    return DownloadData


# 获取全部作者信息和最后更新时间
def GetAllAuthorAndRecordIndo():
    conn = sqlite3.connect('Download.db')
    sql = 'select * from author; '
    with conn:
        datas = conn.execute(sql, )
        for info in datas:
            da = (info[0], info[2], info[1], info[3])
            DownloadData.append(da)
    conn.close()
    return DownloadData


# 更新全部作者信息和最后更新时间 高效率
def UpdateAllAuthorAndRecordIndo(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'REPLACE INTO author (id,user_id,author,time) values(?,?,?,?) '
    cursor = conn.cursor()
    # with conn:
    cursor.executemany(sql, datas)
    cursor.close()
    conn.commit()
    conn.close()


def GetAllAuthorInfo():
    conn = sqlite3.connect('Download.db')
    sql = 'select * from author '
    with conn:
        datas = conn.execute(sql, )
        for info in datas:
            da = (info[0], main2.rep_char(info[1]), info[2])
            DownloadData.append(da)
    conn.close()
    return DownloadData


def UpdateAllAuthorInfo(datas):
    conn = sqlite3.connect('Download.db')
    sql = 'REPLACE INTO author (user_id,author,id) values(?,?,?) '
    cursor = conn.cursor()
    # with conn:
    cursor.executemany(sql, datas)
    cursor.close()
    conn.commit()
    conn.close()


def selectIsDownloadDate(url):
    conn = sqlite3.connect('Download.db')
    sql = 'select isDownload from Download  where user_id = ? and time =? '
    with conn:
        datas = conn.execute(sql, url)
        for data in datas:
            return data[0]


def selectUserIdDate(url):
    conn = sqlite3.connect('Download.db')
    # conn.row_factory = sqlite3.Row
    sql = 'select user_id from author  where user_id = ?'
    with conn:
        datas = conn.execute(sql, url)
        return len(list(datas))


def GetUserMaxTime(user_id):
    conn = sqlite3.connect('Download.db')
    # conn.row_factory = sqlite3.Row
    sql = 'SELECT MAX(time) FROM "Download" WHERE user_id= ?and isDownload=1'
    with conn:
        datas = conn.execute(sql, user_id)
        for data in datas:
            return data[0]


# 获取用户存储作品数量
def GetUserWorksNum(user_id):
    conn = sqlite3.connect('Download.db')
    # conn.row_factory = sqlite3.Row
    datas1 = [user_id]
    sql = 'SELECT  COUNT(*)  FROM Download WHERE user_id= ?'
    with conn:
        datas = conn.execute(sql, datas1)
        for data in datas:
            return data[0]


def FillAuthorData():
    conn = sqlite3.connect('Download.db')
    sql = "SELECT user_id FROM author;"
    id_list = []
    fp = open('ID.txt', 'w')
    with conn:
        datas = conn.execute(sql, )
        for data in datas:
            print(data[0], file=fp)
            id_list.append(data[0])
    conn.close()
    return id_list


def FillAuthorDataTimeZero():
    conn = sqlite3.connect('Download.db')
    sql = "SELECT user_id FROM author where time='0';"
    id_list = []
    fp = open('ID.txt', 'w')
    with conn:
        datas = conn.execute(sql, )
        for data in datas:
            print(data[0], file=fp)
            id_list.append(data[0])
    conn.close()
    return id_list


# 通过Author表读取用户最新时间
def GetTimeDataForAuthor(author):
    conn = sqlite3.connect('Download.db')
    sql = 'select time FROM author WHERE user_id=?;'
    datas1 = [author]
    with conn:
        datas = conn.execute(sql, datas1)
        for data in datas:
            if data[0] is None:
                return "0"
            else:
                return data[0]


# 通过Download表读取用户最新时间
def GetTimeDataForDownload(author):
    conn = sqlite3.connect('Download.db')
    sql = 'SELECT  time FROM Download WHERE user_id=? ORDER BY time DESC;'
    # sql = 'SELECT MAX(Download.time) FROM Download WHERE user_id =? ;'

    datas1 = [author]
    with conn:
        datas = conn.execute(sql, datas1)
        for data in datas:
            if data[0] is None:
                return "0"
            else:
                return data[0]


# 更新最新作品时间
def UpdateAuthorTime(user_id, time):
    conn = sqlite3.connect('Download.db')
    datas1 = [(time, user_id)]
    sql = 'Update  author set  time = ? where user_id = ? '
    with conn:
        conn.executemany(sql, datas1)
    conn.close()


# 压缩数据库
def CompressDataBase():
    conn = sqlite3.connect('Download.db')
    sql = 'vacuum; '
    conn.execute(sql, )


# 删除重复数据 Author
def DeleteRepetitionDataForAuthor():
    conn = sqlite3.connect('Download.db')
    sql = 'delete from author where author.rowid  not in (select MAX(author.rowid ) from author group by user_id);; '
    conn.execute(sql, )


def DeleteInvalidDataForAuthor(user_id):
    conn = sqlite3.connect('Download.db')
    sql = 'delete from author where user_id=?; '
    datas1 = [user_id]
    conn.execute(sql, datas1)


def DeleteInvalidDataForDownload(user_id):
    conn = sqlite3.connect('Download.db')
    sql = 'delete from Download where user_id=?; '
    datas1 = [user_id]
    conn.execute(sql, datas1)


# 下载信息
DownloadData = []
num = 0
def func(user_id, video_url, video_time, isDownload, video_name, id, author):
    # time.sleep(0.5)
    global num
    if not os.path.exists(path + '/' + author + '/'):
        os.makedirs(path + '/' + author + '/')
    datas = [user_id, video_time]
    num += 1
    filepath = path + '/' + author + '/' + str(video_time) + '-' + video_name + '.mp4'
    if selectIsDownloadDate(datas) == 0 and not os.path.exists(filepath):
        if video_url != "":
            video_content = requests.get(video_url, timeout=6.8).content
            with open(filepath, mode='wb') as f:
                f.write(video_content)
            # UpdateDate(datas)
        print(f'{str(num) + "# " + filepath}>>> 下载完成')
    else:
        print(f'{str(num) + "# " + filepath}>>> 已存在')
    # datas = (user_id, video_url, video_time,True,video_name,id)
    datas = (user_id, '', video_time, True, '', id)  # 下载完成后删url地址和作品名称 减小数据库大小
    DownloadData.append(datas)


def GetMaxTime():
    a = []
    i = 0
    conn = sqlite3.connect('Download.db')
    # conn.row_factory = sqlite3.Row
    sql = 'select user_id ,time from author'
    with conn:
        datas = conn.execute(sql)
        for d in datas:
            if d[1] != '0':
                s = [d[0], 1]
                # print(d[0])
                sql1 = 'SELECT MAX(time) FROM "Download" WHERE user_id= ?and isDownload=?'
                with conn:
                    datas2 = conn.execute(sql1, s)
                    for d2 in datas2:
                        i += 1
                        s2 = [d[0], d2[0]]
                        print("#", i, s2)
                sql2 = ' DELETE FROM Download WHERE user_id= ? and time !=  ?;'
                with conn:
                    conn.execute(sql2, s2)
    CompressDataBase()


def CreateFileDirectory(authors):
    if len(authors) > 0:
        index = 0
        for d in authors:
            if not os.path.exists(path + '/' + authors[index][0][6] + '/'):
                os.makedirs(path + '/' + authors[index][0][6] + '/')
            index += 1


path = 'D:/video'
if __name__ == '__main__':
    # UpdateAllAuthorAndRecordIndo(GetAllAuthorAndRecordIndo())
    pool = threadpool.ThreadPool(50)  # 线程池设置,最多同时跑30个线程
    flag = 0
    print("数据库加载中~~~")
    authors = GetDownloadDate()
    if len(authors) > 0:
        print("视频总数：", len(authors))
        print("目录创建中~~~")
        CreateFileDirectory(authors)
        print("目录创建完成")
        print("开始下载~~~")
        tasks = threadpool.makeRequests(func, authors)
        [pool.putRequest(task) for task in tasks]
        pool.wait()
        print("下载完成")
        print("数据库更新中~~~")
        UpdateDates2(DownloadData)
        print("数据库压缩中~~~")
        CompressDataBase()
        print("数据库更新完成")
    else:
        print("没有新数据~~~")

# create_database()
