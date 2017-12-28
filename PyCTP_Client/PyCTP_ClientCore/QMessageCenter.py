# -*- coding: utf-8 -*-

"""
Module implementing MessageCenter.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget

from Ui_QMessageCenter import Ui_MessageForm


class MessageCenter(QWidget, Ui_MessageForm):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MessageCenter, self).__init__(parent)
        self.setupUi(self)

    # 显示TS连接状态，形参dict_input{'msg': 'TS连接', 'alert': False}或{'msg': 'TS断开', 'alert': True}
    def set_label_TS_connect_text(self, dict_input):
        if dict_input['alert']:  # 红色字体
            msg = "<font color='red'>" + dict_input['msg'] + "</font>"
        else:
            msg = dict_input['msg']
        self.label_TS_connect.setText(msg)
