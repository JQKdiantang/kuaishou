from PyQt5.QtCore import QObject, pyqtSignal


class CusSignal(QObject):
    # 无参数的信号
    signal1 = pyqtSignal()
    # 带一个参数（整数）的信号
    signal2 = pyqtSignal(int)
    # 带两个参数（整数，字符串）的信号
    signal3 = pyqtSignal(int, str)
    # 带一个参数（列表）的信号
    signal4 = pyqtSignal(list)
    # 带一个参数（字典）的信号
    signal5 = pyqtSignal(dict)
    # 带（整数 字符串）或者（字符串）的信号
    signal6 = pyqtSignal([int, str], [str])

    def __init__(self, parent=None):
        super(CusSignal, self).__init__(parent)
        # 信号与槽函数的链接
        self.signal1.connect(self.signalCall1)
        self.signal2.connect(self.signalCall2)
        self.signal3.connect(self.signalCall3)
        self.signal4.connect(self.signalCall4)
        self.signal5.connect(self.signalCall5)
        self.signal6[int, str].connect(self.signalCall6)
        self.signal6[str].connect(self.signalCall7)
        # 信号发射
        self.signal1.emit()
        self.signal2.emit(1)
        self.signal3.emit(1, '第三个')
        self.signal4.emit([1, 2, 3, 4])
        self.signal5.emit({"name": 'JIA', 'age': '21'})
        self.signal6[int, str].emit(1, "第六")
        self.signal6[str].emit('第六')

    # 槽函数
    def signalCall1(self):
        print("signal1 emit")

    def signalCall2(self, val):
        print('signal2 emit,value:', val)

    def signalCall3(self, val, text):
        print('signall3 emit,value:', val, text)

    def signalCall4(self, val):
        print('signal4 emit,value:', val)

    def signalCall5(self, val):
        print('signal5 emit,value', val)

    def signalCall6(self, val, text):
        print('signal6 emit,value', val, text)

    def signalCall7(self, val):
        print('signal6 ovetload emit', val)


if __name__ == '__main__':
    custSignal = CusSignal()