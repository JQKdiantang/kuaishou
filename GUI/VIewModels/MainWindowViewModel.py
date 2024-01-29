import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox

from GUI.DataBase import SQLiteHelper
from GUI.VIewModels.AddAuthorViewModel import AddAuthorVIewModel
from GUI.VIewModels.SettingViewModel import SettingVIewModel
from GUI.VIewModels.DataManagementViewModel import DataManagementViewModel
from GUI.VIews.ViewMainWindow import Ui_MainWindow


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
        self.listInfo = None

        self.btnStart.clicked.connect(self.Gather)
        self.btnAdd.clicked.connect(self.AddAuthor)
        self.btnSet.clicked.connect(self.Setting)
        self.btnData.clicked.connect(self.DataManagement)
        self.btnClose.clicked.connect(self.closeEvent)
        self.Init()

    def Gather(self):
        print(11)

    def AddAuthor(self):
        self.ui_author = AddAuthorVIewModel()
        self.ui_author.setWindowModality(QtCore.Qt.ApplicationModal)
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
        self.tw_author.setColumnWidth(1, 253)
        self.tw_author.setColumnWidth(2, 75)
        self.FullAuthor()

        self.tw_works.setColumnWidth(0, 200)
        self.tw_works.setColumnWidth(1, 100)
        self.tw_works.setColumnWidth(2, 300)

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)
        AuthorDatas = SQLiteHelper.GetAllAuthorInfoNo()
        for data in AuthorDatas:
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            list = [QTableWidgetItem(str(data[0])), QTableWidgetItem(data[1]), QTableWidgetItem("未采集")]
            self.listInfo = [(str(data[0]), data[1], data[2], "未采集")]
            for i in range(len(list)):
                self.tw_author.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))
            checkBox = QCheckBox()
            self.tw_author.setCellWidget(rowIdx, 0, checkBox)  # 将 QCheckBox 设置为单元格小部件


if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = MainWindowViewModel()
    MainWindow.show()
    sys.exit(app.exec_())
