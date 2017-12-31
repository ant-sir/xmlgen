# -*- coding: utf-8 -*-

import os, sys
from PyQt5 import QtWidgets
from frame import Ui_Form
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from clang.cindex import Index, CursorKind
from xml.etree import ElementTree

import platform
if platform.system() == 'Windows':
    from clang.cindex import Config
    Config.set_library_path("C:\\Program Files\\LLVM\\bin")

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
        self.child = None
        self.willgen = {}

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
            parser = ElementTree.XMLParser(target = builder, encoding='UTF-8')
            self.tree = ElementTree.parse(file, parser = parser)
            #ElementTree.dump(self.tree)
            lprocess = self.tree.getiterator('process')
            self.comboBoxSelSecXml.addItem("ALL")
            self.comboBoxSelSecXml.addItems([process.text for process in lprocess])

    def selXmlSection(self, section):
        self.section = section
        if section == 'ALL':
            self.textEditShow.setText(ElementTree.tostring(self.tree.getroot(), encoding='UTF-8').decode('UTF-8'))
        else:
            for child in self.tree.getroot():
                if child[0].text == section:
                    self.child = child
                    self.textEditShow.setText(ElementTree.tostring(child, encoding='UTF-8').decode('UTF-8'))

    def genXmlText(self):
        if not self.child:
            QMessageBox.warning(self, "警告", "必须选择一个进程！", QMessageBox.Ok)
            return
        iitems = self.tableWidgetDest.selectedItems()
        if len(iitems) == 0:
            for row in range(self.tableWidgetDest.rowCount()):
                str_file = self.tableWidgetDest.item(row, 0).text()
                if str_file in self.willgen.keys():
                    self.willgen[str_file].append(self.tableWidgetDest.item(row, 1).text())
                else:
                    self.willgen[str_file] = [self.tableWidgetDest.item(row, 1).text()]
            print(self.willgen)
        else:
            for i in range(0, len(iitems), 2):
                str_file = iitems[i].text()
                if str_file in self.willgen.keys():
                    self.willgen[str_file].append(iitems[i+1].text())
                else:
                    self.willgen[str_file] = [iitems[i+1].text()]
            print(self.willgen)

    def saveXmlFile(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
