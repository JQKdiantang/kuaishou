import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidgetItem, QCheckBox

from GUI.Utils import SQLiteHelper, Util
from GUI.VIewModels.AddAuthorInfo import AddAuthor
from GUI.VIewModels.AddUserInfo import addUser
from GUI.VIews.main import Ui_MainWindow as main_ui


class Main(QMainWindow, main_ui):
    def __init__(self):
        super(Main, self).__init__()
        self.listInfo = None
        self.setupUi(self)
        self.btnStart.clicked.connect(self.Start)
        self.btnAdd.clicked.connect(self.AddAuthor)
        self.btnClose.clicked.connect(self.closeEvent)
        self.Init()
        SQLiteHelper.create_database()

    def Start(self):
        print(11)

    def AddAuthor(self):
        print(11)
        # self.ui_author = AddAuthor()
        # self.ui_author.setWindowModality(QtCore.Qt.ApplicationModal)
        # self.ui_author.show()

        self.ui_user = addUser()
        self.ui_user.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui_user.show()

    def Setting(self):
        print(11)

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
        self.tw_author.setColumnWidth(1, 253)
        self.tw_author.setColumnWidth(2, 75)
        self.FullAuthor()

        self.tw_works.setColumnWidth(0, 200)
        self.tw_works.setColumnWidth(1, 100)
        self.tw_works.setColumnWidth(2, 300)

    def FullAuthor(self):
        
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)

        datas = SQLiteHelper.GetAllAuthorInfoNo()
        print(datas)
        for data in datas:
            print(data[0], data[1],data[2])
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("未下载")]
            self.listInfo =[(str(data[0]),data[1],data[2],"未下载")]
            for i in range(len(list)):
                self.tw_author.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))
            checkBox = QCheckBox()
            self.tw_author.setCellWidget(rowIdx, 0, checkBox)  # 将 QCheckBox 设置为单元格小部件
        # datas.clear()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())

    # app = QApplication(sys.argv)  # 只要是Qt制作的程序，必须有且只有一个QApplication对象
    # # sys.argv当做参数的目的是将运行时的命令参数传递给QApplication对象
    # # 此处调用GUI的程序
    # widgets = QtWidgets.QMainWindow()
    #
    # ui = main.Ui_MainWindow()
    # ui.setupUi(widgets)
    #
    # # 展示窗口
    # widgets.show()  # 调用show方法显示出来
    #
    # # 程序进行循环等待状态
    # app.exec()  # 程序开始运行程序，直到关闭了窗口
