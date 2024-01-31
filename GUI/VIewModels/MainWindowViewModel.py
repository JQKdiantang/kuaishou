import sys
import time

import threadpool
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
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
    finished = pyqtSignal(str)

    def run(self,user_id):
        # 模拟耗时操作
        result = self.save(user_id)
        self.finished.emit(result)

    def save(self, user_id):
        list_info = []
        page = ""
        # 循环下载视频，直到 page == 'no_more'
        while page != 'no_more':
            time.sleep(1)
            page, data_list = kuaishou.getWorksInfo(user_id, page)
            for item in data_list:
                time.sleep(1)
                author = rep_char(item['author']['name'])
                # 视频名称
                video_name = rep_char(item['photo']['caption'])
                # 视频时长
                duration = int(item['photo']['duration'] / 1000)
                # 视频ID
                video_id = item['photo']['videoResource']['h264']['videoId']
                # 视频高度
                video_hieght = item['photo']['videoResource']['h264']['adaptationSet'][0]['representation'][0]['height']
                # 视频宽度
                video_width = item['photo']['videoResource']['h264']['adaptationSet'][0]['representation'][0]['width']
                # self.finished.emit((author, video_name, duration))
                list_info.append((author, video_name, duration))
            return list_info


class MainWindowViewModel(QMainWindow, Ui_MainWindow):
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
        self.Init()

    def Gather(self):
        # pool = threadpool.ThreadPool(3)  # 线程池设置
        # tasks = threadpool.makeRequests(self.save, authors)
        # [pool.putRequest(task) for task in tasks]
        # pool.wait()

        # self.save(self.listInfo[0][2])
        # print(self.listInfo)
        # print(self.listInfo[0][0],self.listInfo[0][1],self.listInfo[0][2])
        self.thread = Worker()
        self.thread.finished.connect(self.on_result_changed)  # 连接信号和槽
        self.thread.run("3xvp8hx2nns2r2k")  # 启动线程

    def on_result_changed(self, result):
        print(result)

        # for author, video_name, duration in result:
        #     self.tw_works.insertRow(self.tw_works.rowCount())
        #     rowIdx = self.tw_works.rowCount() - 1
        #     # list = [QTableWidgetItem(author), QTableWidgetItem(video_name),QTableWidgetItem(str(duration)+'s'),QTableWidgetItem("已下99.9%")]
        #     list = [QTableWidgetItem(author), QTableWidgetItem(video_name), QTableWidgetItem(str(duration) + 's'),
        #             QTableWidgetItem("等待下载")]
        #     for i in range(len(list)):
        #         self.tw_works.setItem(rowIdx, i, list[i])
        #         list[i].setTextAlignment(QtCore.Qt.AlignCenter)
        #         list[i].setForeground(QColor(83, 113, 171))
        #     print(video_name, duration)
    def save(self, user_id):
        page = ""
        # 循环下载视频，直到 page == 'no_more'
        while page != 'no_more':
            time.sleep(0.2)
            page, data_list = kuaishou.getWorksInfo(user_id, page)
            for item in data_list:
                time.sleep(0.2)
                author = rep_char(item['author']['name'])
                # 视频名称
                video_name = rep_char(item['photo']['caption'])
                # 视频时长
                duration = int(item['photo']['duration'] / 1000)
                # 视频ID
                video_id = item['photo']['videoResource']['h264']['videoId']
                # 视频高度
                video_hieght = item['photo']['videoResource']['h264']['adaptationSet'][0]['representation'][0]['height']
                # 视频宽度
                video_width = item['photo']['videoResource']['h264']['adaptationSet'][0]['representation'][0]['width']

                self.tw_works.insertRow(self.tw_works.rowCount())
                rowIdx = self.tw_works.rowCount() - 1
                # list = [QTableWidgetItem(author), QTableWidgetItem(video_name),QTableWidgetItem(str(duration)+'s'),QTableWidgetItem("已下99.9%")]
                list = [QTableWidgetItem(author), QTableWidgetItem(video_name), QTableWidgetItem(str(duration) + 's'),
                        QTableWidgetItem("等待下载")]
                for i in range(len(list)):
                    self.tw_works.setItem(rowIdx, i, list[i])
                    list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                    list[i].setForeground(QColor(83, 113, 171))
                print(video_id, video_name, duration, video_hieght, video_width)
                QApplication.processEvents()
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
        self.tw_works.setColumnWidth(1, 400)
        self.tw_works.setColumnWidth(2, 100)
        self.tw_works.setColumnWidth(3, 100)

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)
        AuthorDatas = SQLiteHelper.GetAllAuthorInfoNo()
        for data in AuthorDatas:
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            # list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("已采集到1000个作品，下载成功1000个")]
            list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("未采集")]
            self.listInfo.append((str(data[0]), data[1], data[2], "未采集"))
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
