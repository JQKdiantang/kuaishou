import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from GUI.Utils import Util
from GUI.DataBase import SQLiteHelper
from GUI.VIews.ViewDataManagement import Ui_DataManagement


class DataManagementViewModel(QMainWindow, Ui_DataManagement):
    signal1 = pyqtSignal()

    def __init__(self):
        super(DataManagementViewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.Add)
        self.btnRemove.clicked.connect(self.Remove)
        self.tw_author.cellDoubleClicked.connect(self.tableWidget_cellClicked)
        self.tw_author_2.cellDoubleClicked.connect(self.tableWidget2_cellClicked)
        self.signal1.connect(self.FullAuthor)

        self.Init()

    def Init(self):
        self.tw_author.setColumnCount(3)
        self.tw_author.setColumnWidth(0, 150)
        self.tw_author.setColumnWidth(1, 228)
        self.tw_author.setColumnWidth(2, 170)
        self.tw_author.setColumnHidden(0, True)

        self.tw_author_2.setColumnCount(3)
        self.tw_author_2.setColumnWidth(0, 150)
        self.tw_author_2.setColumnWidth(1, 228)
        self.tw_author_2.setColumnWidth(2, 170)
        self.tw_author_2.setColumnHidden(0, True)
        self.FullAuthor()

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)
        datas = SQLiteHelper.GetAllAuthorInfoACL(True)
        for data in datas:
            self.tw_author.insertRow(self.tw_author.rowCount())
            rowIdx = self.tw_author.rowCount() - 1
            list = [QTableWidgetItem(data[0]), QTableWidgetItem(data[1])]
            if data[2] == '0':
                list.append(QTableWidgetItem('无'))
            else:
                list.append(QTableWidgetItem(Util.timestamp_to_datetime(data[2])))
            for i in range(len(list)):
                self.tw_author.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))

        for row in range(self.tw_author_2.rowCount()):
            self.tw_author_2.removeRow(0)
        datas = SQLiteHelper.GetAllAuthorInfoACL(False)
        for data in datas:
            self.tw_author_2.insertRow(self.tw_author_2.rowCount())
            rowIdx = self.tw_author_2.rowCount() - 1
            list = [QTableWidgetItem(data[0]), QTableWidgetItem(data[1])]
            if data[2] == '0':
                list.append(QTableWidgetItem('无'))
            else:
                list.append(QTableWidgetItem(Util.timestamp_to_datetime(data[2])))
            for i in range(len(list)):
                self.tw_author_2.setItem(rowIdx, i, list[i])
                list[i].setTextAlignment(QtCore.Qt.AlignCenter)
                list[i].setForeground(QColor(83, 113, 171))

    def tableWidget_cellClicked(self, row, column):
        SQLiteHelper.UpdateAuthorACl(self.tw_author.item(row, 0).text(), False)
        self.signal1.emit()

    def tableWidget2_cellClicked(self, row, column):
        SQLiteHelper.UpdateAuthorACl(self.tw_author_2.item(row, 0).text(), True)
        self.signal1.emit()

    def Add(self):
        # 获取选中行
        selected_ranges = self.tw_author_2.selectedRanges()
        for ranges in selected_ranges:
            for row in range(ranges.topRow(), ranges.bottomRow() + 1):
                SQLiteHelper.UpdateAuthorACl(self.tw_author_2.item(row, 0).text(), True)
        self.signal1.emit()

    def Remove(self):
        # 获取选中行
        selected_ranges = self.tw_author.selectedRanges()
        for ranges in selected_ranges:
            for row in range(ranges.topRow(), ranges.bottomRow() + 1):
                SQLiteHelper.UpdateAuthorACl(self.tw_author.item(row, 0).text(), False)
        self.signal1.emit()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = DataManagementViewModel()
    MainWindow.show()
    sys.exit(app.exec_())
