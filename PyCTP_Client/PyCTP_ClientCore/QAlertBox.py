# -*- coding: utf-8 -*-

"""
Module implementing QAlertBox.py.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget
from PyQt4 import QtGui, QtCore
from Ui_QAlertBox import Ui_Form
from xml.dom import minidom
import os


class QAlertBox(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(QAlertBox, self).__init__(parent)
        self.setupUi(self)
        self.read_xml()  # 读取本地xml文件，关于版本信息
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
        self.hide()

    # 形参：{窗口标题, 消息主体}
    def slot_show_alert(self, dict_input):
        self.setWindowTitle(dict_input['title'])
        self.label.setText(dict_input['main'])
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # this will activate the window
        self.activateWindow()

    # 显示版本信息
    def slot_show_version(self):
        # self.setWindowTitle(dict_input['title'])
        self.setWindowTitle("版本")
        # self.label.setText(dict_input['main'])
        self.label.setText(self.__update_main)
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # this will activate the window
        self.activateWindow()

    # 读取xml文件
    def read_xml(self):
        path = "config/about_version.xml"
        # xml文件不存在跳出
        if os.path.exists(path) is False:
            return
        else:
            self.__xml_exist = True

        # 解析文件employ.xml
        self.__doc_read = minidom.parse(path)
        # 定位到根元素
        self.__root_read = self.__doc_read.documentElement
        # 测试代码，开始修改
        NodeList_date = self.__root_read.getElementsByTagName("date")
        NodeList_update = self.__root_read.getElementsByTagName("update")
        self.__update_date = NodeList_date[0].attributes['date'].value
        list_update = [self.__update_date]
        index = 0
        for i in NodeList_update:
            index += 1
            value = str(index) + ": " + i.attributes['update'].value
            list_update.append(value)
        self.__update_main = '<br />'.join(list_update)
        # format = "<html><div style='float:left;text-align:left'>"
        # format_end = "</div></html>"
        # self.__msg = format + self.__update_main + format_end
        # self.label.setAlignment(QtCore.Qt.AlignLeft)  # 窗体文本设置居左


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    abox = QAlertBox()
    abox.label.setText("haha")  # 消息主体
    abox.setWindowTitle("提示")  # 窗口标题
    abox.show()
    sys.exit(app.exec_())