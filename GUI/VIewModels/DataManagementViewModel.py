import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from GUI.Utils import Util
from GUI.DataBase import SQLiteHelper
from GUI.VIews.ViewDataManagement import Ui_DataManagement


class DataManagementViewModel(QMainWindow, Ui_DataManagement):

    def __init__(self):
        super(DataManagementViewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.btnClose.clicked.connect(self.close)
        self.Init()

    def Init(self):
        self.tw_author.setColumnCount(2)

        # self.tw_author.setColumnWidth(0, 150)
        self.tw_author.setColumnWidth(0, 228)
        self.tw_author.setColumnWidth(1, 170)
        self.FullAuthor()

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)
        datas = SQLiteHelper.GetAllAuthorInfo()
        for data in datas:
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            list = [QTableWidgetItem(data[1])]
            if data[2] == '0':
                list.append(QTableWidgetItem('无'))
            else:
                list.append(QTableWidgetItem(Util.timestamp_to_datetime(data[2])))
            for i in range(len(list)):
                self.tw_author.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = DataManagementViewModel()
    MainWindow.show()
    sys.exit(app.exec_())
