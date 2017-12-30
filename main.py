# -*- coding: utf-8 -*-

import os, sys
from PyQt5 import QtWidgets
from frame import Ui_Form
from PyQt5.QtWidgets import QFileDialog
from clang.cindex import Index, CursorKind
from xml.etree import ElementTree

import platform
if platform.system() == 'Windows':
    from clang.cindex import Config
    Config.set_library_path("C:\\Program Files\\LLVM\\bin")

if sys.version_info < (3, 2):
    class CommentedTreeBuilder(ElementTree.XMLTreeBuilder):
        def __init__(self, html = 0, target = None):
            ElementTree.XMLTreeBuilder.__init__(self, html, target)
            self._parser.CommentHandler = self.handle_comment
        
        def handle_comment(self, data):
            self._target.start(ElementTree.Comment, {})
            self._target.data(data)
            self._target.end(ElementTree.Comment)
else:
    class CommentedTreeBuilder(ElementTree.TreeBuilder):
        def __init__(self, factory = None):
            ElementTree.TreeBuilder.__init__(self, factory)

        def comment(self, data):
            self.start(ElementTree.Comment, {})
            self.data(data)
            self.end(ElementTree.Comment)

class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.postfix = ''
        self.tree = None
        self.section = ''

    def insertRow(self, table, file, func):
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(file))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(func))

    def openPatchFiles(self):
        files, ok = QFileDialog.getOpenFileNames(self,
                                                 "选择patch文件",
                                                 "./",
                                                 "C Files (*.c);;All Files (*)")
        index = Index.create()
        for patch_file in files:
            tu = index.parse(patch_file)
            tu_node = tu.cursor.get_children()
            for cursor in tu_node:
                if cursor.kind == CursorKind.FUNCTION_DECL and cursor.is_definition():
                    self.insertRow(self.tableWidgetSource,
                                   os.path.basename(cursor.location.file.name),
                                   cursor.spelling)

    def setLineEditText(self, x, y):
        if x == 0 and y == 1:
            str = self.tableWidgetSource.item(x, y).text()
            self.lineEditPostfix.setText('_' + str.split('_')[-1])

    def changePostfix(self, str):
        self.postfix = str

    def addSelectFunctions(self, x = None, y = None):
        iitems = self.tableWidgetSource.selectedItems()
        litems = list()
        for i in range(0, len(iitems), 2):
            litems.append((iitems[i], iitems[i+1]))
        for item_r, item_c in litems:
            self.insertRow(self.tableWidgetDest, item_r.text(),  item_c.text().split(self.postfix)[0])

    def delSelectFunctions(self, x = None, y = None):
        iitems = self.tableWidgetDest.selectedItems()
        for i in range(0, len(iitems), 2):
            self.tableWidgetDest.removeRow(iitems[i].row())

    def openXmlFile(self):
        file, ok = QFileDialog.getOpenFileName(self,
                                                 "选择cmd.xml文件",
                                                 "./",
                                                 "XML Files (*.xml)")
        if file:
            builder = CommentedTreeBuilder()
            parser = ElementTree.XMLParser(target = builder, encoding='utf-8')
            self.tree = ElementTree.parse(file, parser = parser)
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
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
