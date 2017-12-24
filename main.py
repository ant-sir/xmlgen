# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from frame import Ui_Form
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def openPatchFiles(self):
        files, ok = QFileDialog.getOpenFileNames(self,
                                                 "选择patch文件",
                                                 "C:/",
                                                 "All Files (*);;C Files (*.c)")

    def changePostfix(self):
        pass

    def addSelectFunctions(self):
        pass

    def delSelectFunctions(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())