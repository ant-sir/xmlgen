# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from frame import Ui_Form
from PyQt5.QtWidgets import QFileDialog
from clang.cindex import Index, CursorKind
from xml.etree import ElementTree

class CommentedTreeBuilder(ElementTree.TreeBuilder):
    def __init__(self, html = 0, target = None):
        ElementTree.TreeBuilder.__init__(self, html, target)
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ElementTree.Comment, {})
        self._target.data(data)
        self._target.end(ElementTree.Comment)

class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.postfix = ''
        self.tree = None
        self.section = ''

    def insertRow(self, table, str):
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str))

    def openPatchFiles(self):
        files, ok = QFileDialog.getOpenFileNames(self,
                                                 "选择patch文件",
                                                 "C:/",
                                                 "C Files (*.c);;All Files (*)")
        index = Index.create()
        for patch_file in files:
            tu = index.parse(patch_file, parser = CommentedTreeBuilder())
            tu_node = tu.cursor.get_children()
            for cursor in tu_node:
                if cursor.kind == CursorKind.FUNCTION_DECL and cursor.is_definition():
                    self.insertRow(self.tableWidgetSource, cursor.spelling)

    def setLineEditText(self, x, y):
        if x == 0 and y == 0:
            str = self.tableWidgetSource.item(x, y).text()
            self.lineEditPostfix.setText('_' + str.split('_')[-1])

    def changePostfix(self, str):
        self.postfix = str

    def addSelectFunctions(self, x = None, y = None):
        iitem = self.tableWidgetSource.selectedItems()
        lstr = [item.text().split(self.postfix)[0] for item in iitem if len(item.text()) > 0]
        for str in lstr:
            self.insertRow(self.tableWidgetDest, str)

    def delSelectFunctions(self, x = None, y = None):
        iitem = self.tableWidgetDest.selectedItems()
        for item in iitem:
            self.tableWidgetDest.removeRow(item.row())

    def openXmlFile(self):
        file, ok = QFileDialog.getOpenFileName(self,
                                                 "选择cmd.xml文件",
                                                 "C:/",
                                                 "XML Files (*.xml)")
        if file:
            self.tree = ElementTree.parse(file)
            print(ElementTree.dump(self.tree))
            lprocess = self.tree.getiterator('process')
            self.comboBoxSelSecXml.addItems([process.text for process in lprocess])

    def selXmlSection(self, section):
        self.section = section

    def genXmlText(self):
        pass

    def saveXmlFile(self):
        pass

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
