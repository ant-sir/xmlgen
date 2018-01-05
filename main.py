# -*- coding: utf-8 -*-

import os, sys
from PyQt5 import QtWidgets
from frame import Ui_Form
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from clang.cindex import Index, CursorKind
from lxml import etree

import platform
if platform.system() == 'Windows':
    from clang.cindex import Config
    Config.set_library_path("C:\\Program Files\\LLVM\\bin")

class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.postfix = ''
        self.tree = None
        self.section = ''
        self.pch = None
        self.willgen = {}
        self.xml_file

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
        self.xml_file, ok = QFileDialog.getOpenFileName(self,
                                                 "选择cmd.xml文件",
                                                 "./",
                                                 "XML Files (*.xml)")
        if self.xml_file:
            self.tree = etree.parse(self.xml_file)
            #etree.dump(self.tree.getroot())
            lprocess = [el.text for pch in self.tree.getroot() for el in pch.iterchildren('process')]
            self.comboBoxSelSecXml.addItem("ALL")
            self.comboBoxSelSecXml.addItems(lprocess)

    def selXmlSection(self, section):
        self.section = section
        if section == 'ALL':
            self.textEditShow.setText(etree.tostring(self.tree, encoding='UTF-8', xml_declaration=True, pretty_print=True).decode('UTF-8'))
        else:
            for pch in self.tree.getroot():
                if pch[0].text == section:
                    self.pch = pch
                    self.textEditShow.setText(etree.tostring(self.pch, encoding='UTF-8', pretty_print=True).decode('UTF-8'))
                    break

    def genXmlText(self):
        if self.pch is None:
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
            #print(self.willgen)
        else:
            for i in range(0, len(iitems), 2):
                str_file = iitems[i].text()
                if str_file in self.willgen.keys():
                    self.willgen[str_file].append(iitems[i+1].text())
                else:
                    self.willgen[str_file] = [iitems[i+1].text()]
            #print(self.willgen)
        num = int(list(self.pch.iterchildren('sourceFile'))[-1].attrib['num'])
        for file_name, func_list in self.willgen.items():
            num += 1
            sourceFile = etree.SubElement(self.pch, "sourceFile", attrib={'num' : str(num)})
            sourceFile.text = file_name + 'o' + '\n' + '\t'
            sourceFile.tail = '\n'
            comment = etree.Comment()
            comment_str = '''\n\t补丁函数                             人员     时间        内容描述\n'''
            func_list_str = ''
            for func in func_list:
                func_list_str += '\t' + func + self.postfix + '\n'
            comment.text = comment_str + func_list_str + '\t'
            comment.tail = '\n' + '\t'
            sourceFile.append(comment)
            for i in range(len(func_list)):
                replace = etree.SubElement(sourceFile, "replace", attrib={'num' : str(i+1)})
                replace.text = func_list[i] + self.postfix
                replace.tail = ' '
                replacedname = etree.SubElement(sourceFile, "replacedname")
                replacedname.text = func_list[i]
                replacedname.tail = ' '
                replacedaddr = etree.SubElement(sourceFile, "replacedaddr")
                replacedaddr.text = " "
                replacedaddr.tail = '\n'
                if i != len(func_list) - 1:
                    replacedaddr.tail += '\t'
        #etree.dump(self.pch)
        self.textEditShow.setText(etree.tostring(self.pch, encoding='UTF-8', pretty_print=True).decode('UTF-8'))

    def saveXmlFile(self):
        pch = etree.fromstring(self.textEditShow.toPlainText())
        pch.tail = '\n\n\n'
        self.tree.getroot().replace(self.pch, pch)
        #etree.dump(self.tree.getroot())
        with open(self.xml_file, mode='w', encoding='UTF-8') as fd:
            fd.write(etree.tostring(self.tree, encoding='UTF-8', pretty_print=True).decode('UTF-8'))
        self.textEditShow.setDisabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
