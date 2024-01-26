import re
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView, QAbstractItemView, QTableWidgetItem

from GUI.Utils import SQLiteHelper, kuaishou, Util
from GUI.VIews.AddAuthor import Ui_MainWindow as AddAuthor_ui


class AddAuthor(QMainWindow, AddAuthor_ui):

    def __init__(self):
        super(AddAuthor, self).__init__()
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.Add)
        self.btnClose.clicked.connect(self.close)
        self.Init()

    def Add(self):
        result = ''
        if len(self.lineEdit.text()) == 15:
            result = self.lineEdit.text()
        else:
            match = re.search(r'profile/(.*)', self.lineEdit.text())
            if match:
                result = match.group(1)
        if result == '':
            QMessageBox.information(self, '信息', "输入格式不正确", QMessageBox.Yes)
            return
        datas = [result]
        if SQLiteHelper.selectUserIdDate(datas) != 1:
            photo_public, user_name = kuaishou.getAuthorPublicNum(result)
            print(photo_public, user_name)
            datas = [
                (result, user_name, "0")
            ]
            SQLiteHelper.insertAuthorDate(datas)
            self.FullAuthor()
            QMessageBox.information(self, '信息', "作者添加成功", QMessageBox.Yes)
        else:
            QMessageBox.information(self, '信息', "作者已存在", QMessageBox.Yes)

    def FullAuthor(self):
        for row in range(self.tw_author.rowCount()):
            self.tw_author.removeRow(0)

        datas = SQLiteHelper.GetAllAuthorInfo()
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
        datas.clear()

    def Init(self):
        self.tw_author.setColumnCount(3)
        # self.tw_author.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_author.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tw_author.horizontalHeader().setHighlightSections(False)

        self.tw_author.setColumnWidth(0, 150)
        self.tw_author.setColumnWidth(1, 290)
        self.tw_author.setColumnWidth(2, 170)
        self.FullAuthor()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = AddAuthor()
    MainWindow.show()
    sys.exit(app.exec_())
