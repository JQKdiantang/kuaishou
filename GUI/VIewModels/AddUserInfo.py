import re
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor, QBitmap, QPainter, QPixmap, QPainterPath
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView, QAbstractItemView, QTableWidgetItem
from PyQt5.uic.properties import QtGui

from GUI.Utils import SQLiteHelper, kuaishou, Util
from GUI.VIews.addUser import Ui_MainWindow as addUser_ui


class addUser(QMainWindow, addUser_ui):

    def __init__(self):
        super(addUser, self).__init__()
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.close)
        self.btnAdd.clicked.connect(self.Add)
        self.btnQuery.clicked.connect(self.query)

        self.userInfo = []
        # self.initUI()

    def Add(self):
        print(self.userInfo)
        datas = [self.userInfo[0][0]]

        if SQLiteHelper.selectUserIdDate(datas) != 1:
            print(self.userInfo[0][0], self.userInfo[0][1],  self.userInfo[0][2])
            SQLiteHelper.insertAuthorDate(self.userInfo)
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

    def query(self):
        match = re.search(r'profile/(.*)', self.lineEdit.text())
        if match:
            result = match.group(1)
        elif len(self.lineEdit.text()) == 15:
            result = self.lineEdit.text()
        else:
            name, result = kuaishou.SearchUser(self.lineEdit.text())
        if result == '':
            QMessageBox.information(self, '信息', "输入格式不正确", QMessageBox.Yes)
            return
        fan, follow, photo_public, user_name, gender, headurl = kuaishou.getAuthorPublicNum(result)

        print(fan, follow, photo_public, user_name, gender, headurl)

        self.userInfo = [(result, user_name, "0")]

        self.lbl_name.setText(user_name)
        if gender == 'F':
            self.lbl_gender.setPixmap(QPixmap("../Res/female.png"))
        elif gender == 'M':
            self.lbl_gender.setPixmap(QPixmap("../Res/male.png"))
        else:
            self.lbl_gender.setPixmap(QPixmap())
        # self.lbl_gender.setPixmap(QtGui.QPixmap("../Res/female.png" if gender=='F' else "../Res/male.png"))
        # self.lbl_gender.setVisible(True if gender=='F' else False)
        self.lbl_fan.setText(fan)
        self.lbl_photo.setText(photo_public)
        self.lbl_follow.setText(str(follow))
        self.manager = QNetworkAccessManager()
        self.reply = None

        self.manager.finished.connect(self.onFinished)
        self.manager.get(QNetworkRequest(QUrl(headurl)))

    def initUI(self):
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 设置无边框窗口
        # self.setMask(self.createRoundMask())
        self.lbl_gender.setVisible(False)

    def onFinished(self, reply):
        if reply.error() == QNetworkReply.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            self.lbl_head.setPixmap(pixmap)
            self.lbl_head.setMask(self.create_mask())
        else:
            print("Error: ", reply.errorString())
        reply.deleteLater()

    def create_mask(self):
        mask = QBitmap(self.lbl_head.size())
        mask.fill(Qt.white)  # 初始填充白色背景
        painter = QPainter()
        painter.begin(mask)
        path = QPainterPath()
        painter.setRenderHint(QPainter.Antialiasing)

        path.addEllipse(0, 0, mask.width(), mask.height())  # 画一个完整的椭圆作为蒙版
        painter.fillPath(path, Qt.black)  # 将椭圆路径填充为黑色，形成蒙版

        painter.end()
        return mask


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = addUser()
    MainWindow.show()
    sys.exit(app.exec_())
