import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from GUI.VIews.ViewSetting import Ui_Setting


class SettingVIewModel(QMainWindow, Ui_Setting):

    def __init__(self):
        super(SettingVIewModel, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setupUi(self)




if __name__ == '__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = SettingVIewModel()
    MainWindow.show()
    sys.exit(app.exec_())
