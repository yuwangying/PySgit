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
        self.setWindowTitle("版本信息")
        # self.label.setText(dict_input['main'])
        self.label.setText("1.0.2")
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # this will activate the window
        self.activateWindow()

    # # 读取xml文件
    # def read_xml(self):
    #     # xml文件不存在跳出
    #     if os.path.exists("config/about_version.xml") is False:
    #         return
    #     else:
    #         self.__xml_exist = True
    #
    #     # 解析文件employ.xml
    #     self.__doc_read = minidom.parse(self.__path)
    #     # 定位到根元素
    #     self.__root_read = self.__doc_read.documentElement
    #
    #     # 测试代码，开始修改
    #     self.__path_write_start = "config/bee_config_start.xml"
    #     NodeList_user_save_info = self.__root_read.getElementsByTagName("user_write_xml_status")
    #     for i in NodeList_user_save_info:
    #         dt = datetime.now().strftime('%Y-%m-%d %I:%M:%S')
    #         i.attributes['datetime'] = dt
    #     f = open(self.__path_write_start, 'w')
    #     self.__doc_read.writexml(f, encoding='utf-8')  # addindent='  ', newl='\n',
    #     f.close()
    #     # self.__root_read.getElementsByTagName("user_save_info")
    #     self.read_user_save_info()
    #     self.read_user_instrument_statistics()
    #     self.read_strategy_arguments()
    #     self.read_strategy_statistics()
    #     self.read_position_detail_for_order()
    #     self.read_position_detail_for_trade()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    abox = QAlertBox()
    abox.label.setText("haha")  # 消息主体
    abox.setWindowTitle("提示")  # 窗口标题
    abox.show()
    sys.exit(app.exec_())