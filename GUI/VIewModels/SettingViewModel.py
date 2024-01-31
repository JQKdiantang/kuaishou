import configparser
import os
import sys
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.uic.Compiler.qtproxies import QtCore

from GUI.Models import InIData
from GUI.Utils import Util
from GUI.VIews.ViewSetting import Ui_Setting


class SettingVIewModel(QMainWindow, Ui_Setting):

    def __init__(self):
        super(SettingVIewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.open)
        self.btnSelect.clicked.connect(self.select)
        self.btnSave.clicked.connect(self.save)
        self.btnClose.clicked.connect(self.closeEvent)
        self.init()

    def init(self):
        self.read_config_value()
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

    def save(self):
        config_file = "./config.ini"
        # 打开INI文件
        config = configparser.ConfigParser()
        config.read(config_file, encoding='GBK')
        # 修改内容
        config['采集设置']['保存路径（不填则默认）'] = self.lineEdit.text()
        # 保存更改
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    def updateDiskShow(self, converted_path):
        total_gb, used_gb, free_gb, usage_percentage = Util.get_disk_usage(converted_path)
        self.progressBar.setValue(usage_percentage)
        self.progressBar.setFormat(f'已使用 {used_gb} GB/{total_gb} GB 剩余可用 {free_gb} GB')

    def read_config_value(self):
        config_file = "./config.ini"
        # 创建配置解析器对象
        config = configparser.ConfigParser()
        config.read(config_file, encoding='GBK')
        # 检查文件是否存在
        if not os.path.isfile('config.ini'):
            if '采集设置' not in config.sections():
                config.add_section('采集设置')
                config.set('采集设置', '保存路径（不填则默认）', InIData.video_save_path)
                config.set('采集设置', '同时采集线程数', '3')
                config.set('采集设置', '采集作者作品前对比保存作品数与最新作品数', '是')
                config.set('采集设置', '采集作者作品时检测上次采集的最后作品时间', '是')
                config.set('采集设置', '使用随机User-Agent', '是')
                config.set('采集设置', '获取作品的格式：', 'H264')
                # 保存到文件
                with open(config_file, 'w', encoding='GBK') as configfile:
                    config.write(configfile)

        # 读取INI文件
        section = '采集设置'
        key = '保存路径（不填则默认）'
        InIData.video_save_path = value = config.get(section, key)
        self.lineEdit.setText(value)
        # print(f'{section}中的{key}: {value}')

    # options = {"是": True, "否": False}


if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = SettingVIewModel()
    MainWindow.show()
    sys.exit(app.exec_())
