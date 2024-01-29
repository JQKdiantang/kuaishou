import os
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
        self.updateDiskShow(self.lineEdit.text())

    def open(self):
        # 获取文件夹路径
        folder_path = self.lineEdit.text()
        # 检查并创建文件夹（如果不存在）
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 打开文件夹
        os.startfile(folder_path)

    def select(self):
        # 创建文件对话框，并设置对话框类型为选择目录
        # 打开文件夹选择器
        folder_dialog = QFileDialog()
        folder_dialog.setDirectory(self.lineEdit.text())
        folder_dialog.setFileMode(QFileDialog.Directory)  # 设置选择模式为文件夹
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)  # 只显示文件夹，不显示文件

        # 显示文件夹选择器
        if folder_dialog.exec_():
            # 获取所选文件夹的路径
            selected_folder = folder_dialog.selectedFiles()[0]
            # 将反斜杠转换为双反斜杠
            converted_path = selected_folder.replace("/", "\\")
            self.lineEdit.setText(converted_path)
            self.updateDiskShow(converted_path)

    def updateDiskShow(self, converted_path):
        total_gb, used_gb, free_gb, usage_percentage = Util.get_disk_usage(converted_path)
        self.progressBar.setValue(usage_percentage)
        self.progressBar.setFormat(f'已使用 {used_gb} GB/{total_gb} GB 剩余可用 {free_gb} GB')


if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = SettingVIewModel()
    MainWindow.show()
    sys.exit(app.exec_())
