import sys
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import threadpool
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QThreadPool

from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from GUI.DataBase import SQLiteHelper
from GUI.Models import InIData
from GUI.Utils import kuaishou
from GUI.Utils.Util import rep_char
from GUI.VIewModels.AddAuthorViewModel import AddAuthorVIewModel
from GUI.VIewModels.SettingViewModel import SettingVIewModel
from GUI.VIewModels.DataManagementViewModel import DataManagementViewModel
from GUI.VIews.ViewMainWindow import Ui_MainWindow


class Worker(QThread):
    finished = pyqtSignal(list)

    def run(self, user_id):
        print(user_id)
        result = self.save(user_id)

    def save(self, user_id):
        num = 0
        page = ""
        # 循环下载视频，直到 page == 'no_more'
        while page != 'no_more':
            list_info = []
            page, data_list = kuaishou.getWorksInfo(user_id, page)
            # self.finished.emit(data_list)
            for item in data_list:
                num += 1
                author = rep_char(item['author']['name'])
                # 视频名称
                video_name = rep_char(item['photo']['caption'])
                # 视频时长
                duration = int(item['photo']['duration'] / 1000)
                video_id = item['photo']['videoResource']['h264']['videoId']

                # 视频地址 H265
                video_url = item['photo']['photoH265Url']
                if video_url is None or video_url == "":  # 如果没有H265 获取H264
                    video_url = item['photo']['photoUrl']
                list_info.append((author, video_name, duration, video_id, video_url))

            self.finished.emit(list_info)


class MainWindowViewModel(QMainWindow, Ui_MainWindow):
    signal1 = pyqtSignal(list)

    def __init__(self):
        super(MainWindowViewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # font_family = "Ryanの阿里媽媽方圓體100"  # 替换为你的字体家族名称
        FontDb = QFontDatabase()
        FontID = FontDb.addApplicationFont(":/font/阿里妈妈方圆体100.ttf")
        FontFamily = FontDb.applicationFontFamilies(FontID)
        self.setFont(QFont(FontFamily[0]))
        # 创建数据库
        SQLiteHelper.create_database()

        self.setupUi(self)
        self.ui_author = None
        self.ui_setting = None
        self.ui_data = None
        self.listInfo = []

        self.btnStart.clicked.connect(self.Gather)
        self.btnAdd.clicked.connect(self.AddAuthor)
        self.btnSet.clicked.connect(self.Setting)
        self.btnData.clicked.connect(self.DataManagement)
        self.btnClose.clicked.connect(self.closeEvent)
        self.signal1.connect(self.on_result_changed)
        self.Init()

    def Gather(self):
        # self.thread = Worker()
        # self.thread.setTerminationEnabled(True)  # 设置线程可终止
        # self.thread.moveToThread(self.thread)  # 将标签组件移动到工作线程中
        # self.thread.finished.connect(self.on_result_changed)  # 连接信号和槽，更新标签文本
        # self.thread.run(authors[0])  # 启动线程

        self.pool = ThreadPoolExecutor(max_workers=1)  # 创建线程池，最大同时运行2个线程
        futures = []  # 用于存储Future对象
        for data in self.listInfo:  # 创建10个Worker线程
            if data[3] == '等待采集':
                self.worker = Worker()
                print(data)
                self.worker.finished.connect(self.on_result_changed)  # 连接信号和槽，更新标签文本
                futures = self.pool.submit(self.worker.run(data[2]))  # 提交任务到线程池


    # def closeEvent(self, event):  # 重写关闭事件处理函数，确保线程池关闭并处理完信号再关闭窗口
    #     self.pool.shutdown()  # 关闭线程池
    #     event.accept()  # 接受关闭事件

    def on_result_changed(self, list_info):
        for author, video_name, duration, video_id, video_url in list_info:
            self.tw_works.insertRow(self.tw_works.rowCount())
            rowIdx = self.tw_works.rowCount() - 1
            list = [QTableWidgetItem(author), QTableWidgetItem(video_name), QTableWidgetItem(str(duration)),
                    QTableWidgetItem("等待下载")]
            for i in range(len(list)):
                self.tw_works.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[1].setForeground(QColor(83, 113, 171))
            QApplication.processEvents()  # 处理事件队列，确保界面更新

    def save(self, user_id):
        page = ""
        # 循环下载视频，直到 page == 'no_more'
        while page != 'no_more':
            list_info = []
            time.sleep(1)
            page, data_list = kuaishou.getWorksInfo(user_id, page)
            for item in data_list:
                QApplication.processEvents()
                author = rep_char(item['author']['name'])
                # 视频名称
                video_name = rep_char(item['photo']['caption'])
                # 视频时长
                duration = int(item['photo']['duration'] / 1000)
                # 视频ID
                video_id = item['photo']['videoResource']['h264']['videoId']
                # 视频地址 H265
                video_url = item['photo']['photoH265Url']
                if video_url is None or video_url == "":  # 如果没有H265 获取H264
                    video_url = item['photo']['photoUrl']
                list_info.append((author, video_name, duration, video_id, video_url))
            print("采集作品：", list_info)
            self.signal1.emit(list_info)

            # self.tw_works.insertRow(self.tw_works.rowCount())
            # rowIdx = self.tw_works.rowCount() - 1
            # # list = [QTableWidgetItem(author), QTableWidgetItem(video_name),QTableWidgetItem(str(duration)+'s'),QTableWidgetItem("已下99.9%")]
            # list = [QTableWidgetItem(author), QTableWidgetItem(video_name), QTableWidgetItem(str(duration) + 's'),
            #         QTableWidgetItem("等待下载")]
            # for i in range(len(list)):
            #     self.tw_works.setItem(rowIdx, i, list[i])
            #     list[i].setTextAlignment(QtCore.Qt.AlignCenter)
            #     list[i].setForeground(QColor(83, 113, 171))
            # print(video_id, video_name, duration, video_hieght, video_width)

            # # 视频地址 H265
            # video_url = item['photo']['photoH265Url']
            # if video_url is None or video_url == "":  # 如果没有H265 获取H264
            #     video_url = item['photo']['photoUrl']
            #
            # # 视频发布时间
            # video_time = item['photo']['timestamp']
            # # 作者名称
            # author = rep_char(item['author']['name'])

            # # 保存视频地址
            # datas = [id, video_id]
            # if SQLiteHelper.selectIsDownloadDate(datas) != 1:
            #     datas = [(id, video_id)]
            #     SQLiteHelper.insertDownloadDate(datas)

    def AddAuthor(self):
        self.ui_author = AddAuthorVIewModel()
        self.ui_author.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui_author.signal1.connect(self.FullAuthor)
        self.ui_author.show()

    def Setting(self):
        self.ui_setting = SettingVIewModel()
        self.ui_setting.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui_setting.show()

    def DataManagement(self):
        self.ui_data = DataManagementViewModel()
        self.ui_data.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui_data.signal1.connect(self.FullAuthor)
        self.ui_data.show()

    def Download(self):
        print(11)

    def SaveDownloadList(self):
        print(11)

    def importDownloadList(self):
        print(11)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '信息',
                                               "是否退出?",
                                               QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.close()

    def Init(self):
        self.tw_author.setColumnCount(3)
        self.tw_author.setColumnWidth(0, 50)
        self.tw_author.setColumnWidth(1, 200)
        self.tw_author.setColumnWidth(2, 260)
        self.FullAuthor()

        self.tw_works.setColumnWidth(0, 200)
        self.tw_works.setColumnWidth(1, 420)
        self.tw_works.setColumnWidth(2, 80)
        self.tw_works.setColumnWidth(3, 100)

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)
        AuthorDatas = SQLiteHelper.GetAllAuthorInfoNo()
        for data in AuthorDatas:
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            # list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("已采集到1000个作品，下载成功1000个")]
            list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("等待采集")]
            self.listInfo.append((str(data[0]), data[1], data[2], "等待采集"))
            for i in range(len(list)):
                self.tw_author.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))
            # checkBox = QCheckBox()
            # self.tw_author.setCellWidget(rowIdx, 0, checkBox)  # 将 QCheckBox 设置为单元格小部件


if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = MainWindowViewModel()
    MainWindow.show()
    sys.exit(app.exec_())
