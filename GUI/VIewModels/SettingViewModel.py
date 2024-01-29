import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.uic.Compiler.qtproxies import QtCore

from GUI.Utils import Util
from GUI.VIews.ViewSetting import Ui_Setting


class SettingVIewModel(QMainWindow, Ui_Setting):

    def __init__(self):
        super(SettingVIewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.open)
        self.btnSelect.clicked.connect(self.select)
        self.init()

    def init(self):
        # Util.get_disk_usage(self.lineEdit.text())
        print(11)

    def open(self):
        print(11)

    def select(self):
        # 创建文件对话框，并设置对话框类型为选择目录
        directory_dialog = QFileDialog()
        directory_dialog.setFileMode(QFileDialog.Directory)

        # 显示文件对话框
        directory_dialog.show()

        # 获取选择的目录路径
        if directory_dialog.exec_():
            selected_directory = directory_dialog.selectedFiles()[0]
            print(selected_directory)
            self.lineEdit.setText(selected_directory)
            # Util.get_disk_usage(selected_directory)


if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = SettingVIewModel()
    MainWindow.show()
    sys.exit(app.exec_())
