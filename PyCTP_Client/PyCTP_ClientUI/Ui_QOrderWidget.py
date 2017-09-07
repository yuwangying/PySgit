# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CTP\Sgit\PyCTP_Client\PyCTP_ClientUI\QOrderWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1425, 326)
        Form.setStyleSheet(_fromUtf8("QTabWidget::pane { /* The tab widget frame */\n"
"      border-top: 2px solid #C2C7CB;\n"
"}\n"
"\n"
"  QTabWidget::tab-bar {\n"
"      left: 5px; /* move to the right by 5px */\n"
"  }\n"
"\n"
"  /* Style the tab using the tab sub-control. Note that\n"
"      it reads QTabBar _not_ QTabWidget */\n"
"  QTabBar::tab {\n"
"        \n"
"    font: 11pt \"微软雅黑\";\n"
"      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                  stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                  stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"      border: 2px solid #C4C4C3;\n"
"      border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"      border-top-left-radius: 4px;\n"
"      border-top-right-radius: 4px;\n"
"      min-width: 100px;\n"
"      padding: 2px;\n"
"  }\n"
"\n"
"  QTabBar::tab:selected, QTabBar::tab:hover {\n"
"      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                  stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                  stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"  }\n"
"\n"
"  QTabBar::tab:selected {\n"
"      border-color: #9B9B9B;\n"
"      border-bottom-color: #C2C7CB; /* same as pane color */\n"
"  }\n"
"\n"
"  QTabBar::tab:!selected {\n"
"      margin-top: 2px; /* make non-selected tabs look smaller */\n"
"  }\n"
"\n"
"\n"
"/*鼠标右击菜单样式*/\n"
"QMenu {\n"
"      background-color: #ABABAB; /* sets background of the menu */\n"
"      border: 1px solid black;\n"
"  }\n"
"\n"
"  QMenu::item {\n"
"      /* sets background of menu item. set this to something non-transparent\n"
"          if you want menu color and menu item color to be different */\n"
"      background-color: transparent;\n"
"  }\n"
"\n"
"  QMenu::item:selected { /* when user selects item using mouse or keyboard */\n"
"      background-color: #654321;\n"
"  }\n"
"\n"
"/*右下角托盘样式*/\n"
"  QMenuBar {\n"
"      background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                        stop:0 lightgray, stop:1 darkgray);\n"
"  }\n"
"\n"
"  QMenuBar::item {\n"
"      spacing: 3px; /* spacing between menu bar items */\n"
"      padding: 1px 4px;\n"
"      background: transparent;\n"
"      border-radius: 4px;\n"
"  }\n"
"\n"
"  QMenuBar::item:selected { /* when selected using mouse or keyboard */\n"
"      background: #a8a8a8;\n"
"  }\n"
"\n"
"  QMenuBar::item:pressed {\n"
"      background: #888888;\n"
"  }\n"
"\n"
""))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.splitter_2 = QtGui.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setHandleWidth(4)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_account_id = QtGui.QLabel(self.groupBox)
        self.label_account_id.setObjectName(_fromUtf8("label_account_id"))
        self.horizontalLayout.addWidget(self.label_account_id)
        self.comboBox_account_id = QtGui.QComboBox(self.groupBox)
        self.comboBox_account_id.setObjectName(_fromUtf8("comboBox_account_id"))
        self.horizontalLayout.addWidget(self.comboBox_account_id)
        self.label_strategy_id = QtGui.QLabel(self.groupBox)
        self.label_strategy_id.setObjectName(_fromUtf8("label_strategy_id"))
        self.horizontalLayout.addWidget(self.label_strategy_id)
        self.comboBox_strategy_id = QtGui.QComboBox(self.groupBox)
        self.comboBox_strategy_id.setObjectName(_fromUtf8("comboBox_strategy_id"))
        self.horizontalLayout.addWidget(self.comboBox_strategy_id)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tableView_order = QtGui.QTableView(self.splitter)
        self.tableView_order.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 245);"))
        self.tableView_order.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_order.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_order.setObjectName(_fromUtf8("tableView_order"))
        self.tableView_trade = QtGui.QTableView(self.splitter)
        self.tableView_trade.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 245);"))
        self.tableView_trade.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_trade.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_trade.setObjectName(_fromUtf8("tableView_trade"))
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.groupBox_order_insert = QtGui.QGroupBox(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_order_insert.sizePolicy().hasHeightForWidth())
        self.groupBox_order_insert.setSizePolicy(sizePolicy)
        self.groupBox_order_insert.setMinimumSize(QtCore.QSize(325, 0))
        self.groupBox_order_insert.setMaximumSize(QtCore.QSize(325, 16777215))
        self.groupBox_order_insert.setAutoFillBackground(False)
        self.groupBox_order_insert.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 245);"))
        self.groupBox_order_insert.setObjectName(_fromUtf8("groupBox_order_insert"))
        self.label_buyorsell = QtGui.QLabel(self.groupBox_order_insert)
        self.label_buyorsell.setGeometry(QtCore.QRect(8, 69, 30, 16))
        self.label_buyorsell.setObjectName(_fromUtf8("label_buyorsell"))
        self.lineEdit_heyue = QtGui.QLineEdit(self.groupBox_order_insert)
        self.lineEdit_heyue.setGeometry(QtCore.QRect(70, 21, 117, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_heyue.sizePolicy().hasHeightForWidth())
        self.lineEdit_heyue.setSizePolicy(sizePolicy)
        self.lineEdit_heyue.setObjectName(_fromUtf8("lineEdit_heyue"))
        self.label_heyue = QtGui.QLabel(self.groupBox_order_insert)
        self.label_heyue.setGeometry(QtCore.QRect(8, 32, 30, 16))
        self.label_heyue.setObjectName(_fromUtf8("label_heyue"))
        self.radioButton_kaicang = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_kaicang.setGeometry(QtCore.QRect(70, 93, 57, 19))
        self.radioButton_kaicang.setObjectName(_fromUtf8("radioButton_kaicang"))
        self.radioButton_maichu = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_maichu.setGeometry(QtCore.QRect(130, 69, 57, 19))
        self.radioButton_maichu.setObjectName(_fromUtf8("radioButton_maichu"))
        self.label_kaiping = QtGui.QLabel(self.groupBox_order_insert)
        self.label_kaiping.setGeometry(QtCore.QRect(8, 93, 30, 16))
        self.label_kaiping.setObjectName(_fromUtf8("label_kaiping"))
        self.label_shoushu = QtGui.QLabel(self.groupBox_order_insert)
        self.label_shoushu.setGeometry(QtCore.QRect(8, 117, 30, 16))
        self.label_shoushu.setObjectName(_fromUtf8("label_shoushu"))
        self.radioButton_pingcang = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_pingcang.setGeometry(QtCore.QRect(130, 93, 57, 19))
        self.radioButton_pingcang.setObjectName(_fromUtf8("radioButton_pingcang"))
        self.spinBox_shoushu = QtGui.QSpinBox(self.groupBox_order_insert)
        self.spinBox_shoushu.setGeometry(QtCore.QRect(70, 117, 42, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_shoushu.sizePolicy().hasHeightForWidth())
        self.spinBox_shoushu.setSizePolicy(sizePolicy)
        self.spinBox_shoushu.setObjectName(_fromUtf8("spinBox_shoushu"))
        self.radioButton_pingjin = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_pingjin.setGeometry(QtCore.QRect(192, 93, 57, 19))
        self.radioButton_pingjin.setObjectName(_fromUtf8("radioButton_pingjin"))
        self.radioButton_mairu = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_mairu.setGeometry(QtCore.QRect(70, 69, 57, 19))
        self.radioButton_mairu.setObjectName(_fromUtf8("radioButton_mairu"))
        self.doubleSpinBox_xiadanjiage = QtGui.QDoubleSpinBox(self.groupBox_order_insert)
        self.doubleSpinBox_xiadanjiage.setGeometry(QtCore.QRect(70, 157, 90, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_xiadanjiage.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_xiadanjiage.setSizePolicy(sizePolicy)
        self.doubleSpinBox_xiadanjiage.setMaximum(99999.0)
        self.doubleSpinBox_xiadanjiage.setProperty("value", 12345.67)
        self.doubleSpinBox_xiadanjiage.setObjectName(_fromUtf8("doubleSpinBox_xiadanjiage"))
        self.label_xiadanjiage = QtGui.QLabel(self.groupBox_order_insert)
        self.label_xiadanjiage.setGeometry(QtCore.QRect(8, 157, 30, 16))
        self.label_xiadanjiage.setObjectName(_fromUtf8("label_xiadanjiage"))
        self.pushButton_xiadantiaocang = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiadantiaocang.setGeometry(QtCore.QRect(192, 251, 93, 28))
        self.pushButton_xiadantiaocang.setObjectName(_fromUtf8("pushButton_xiadantiaocang"))
        self.pushButton_xiandan = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiandan.setGeometry(QtCore.QRect(8, 218, 181, 61))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_xiandan.sizePolicy().hasHeightForWidth())
        self.pushButton_xiandan.setSizePolicy(sizePolicy)
        self.pushButton_xiandan.setObjectName(_fromUtf8("pushButton_xiandan"))
        self.pushButton_xiadanquxiao = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiadanquxiao.setGeometry(QtCore.QRect(192, 218, 93, 28))
        self.pushButton_xiadanquxiao.setObjectName(_fromUtf8("pushButton_xiadanquxiao"))
        self.label_pankouguadansell = QtGui.QLabel(self.groupBox_order_insert)
        self.label_pankouguadansell.setGeometry(QtCore.QRect(192, 157, 95, 16))
        self.label_pankouguadansell.setObjectName(_fromUtf8("label_pankouguadansell"))
        self.label_dietingjia = QtGui.QLabel(self.groupBox_order_insert)
        self.label_dietingjia.setGeometry(QtCore.QRect(192, 178, 55, 16))
        self.label_dietingjia.setObjectName(_fromUtf8("label_dietingjia"))
        self.label_zuidashoushu = QtGui.QLabel(self.groupBox_order_insert)
        self.label_zuidashoushu.setGeometry(QtCore.QRect(192, 117, 23, 16))
        self.label_zuidashoushu.setObjectName(_fromUtf8("label_zuidashoushu"))
        self.label_zhangtingjia = QtGui.QLabel(self.groupBox_order_insert)
        self.label_zhangtingjia.setGeometry(QtCore.QRect(192, 137, 55, 16))
        self.label_zhangtingjia.setObjectName(_fromUtf8("label_zhangtingjia"))
        self.label_pankouguadanbuy = QtGui.QLabel(self.groupBox_order_insert)
        self.label_pankouguadanbuy.setGeometry(QtCore.QRect(192, 198, 103, 16))
        self.label_pankouguadanbuy.setObjectName(_fromUtf8("label_pankouguadanbuy"))
        self.checkBox_taoli = QtGui.QCheckBox(self.groupBox_order_insert)
        self.checkBox_taoli.setGeometry(QtCore.QRect(192, 21, 57, 19))
        self.checkBox_taoli.setObjectName(_fromUtf8("checkBox_taoli"))
        self.checkBox_baozhi = QtGui.QCheckBox(self.groupBox_order_insert)
        self.checkBox_baozhi.setGeometry(QtCore.QRect(192, 45, 57, 19))
        self.checkBox_baozhi.setObjectName(_fromUtf8("checkBox_baozhi"))
        self.horizontalLayout_3.addWidget(self.splitter_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_account_id.setText(_translate("Form", "期货账号", None))
        self.label_strategy_id.setText(_translate("Form", "策略编号", None))
        self.groupBox_order_insert.setTitle(_translate("Form", "下单板", None))
        self.label_buyorsell.setText(_translate("Form", "买卖", None))
        self.lineEdit_heyue.setText(_translate("Form", "cu1601", None))
        self.label_heyue.setText(_translate("Form", "合约", None))
        self.radioButton_kaicang.setText(_translate("Form", "开仓", None))
        self.radioButton_maichu.setText(_translate("Form", "卖出", None))
        self.label_kaiping.setText(_translate("Form", "开平", None))
        self.label_shoushu.setText(_translate("Form", "手数", None))
        self.radioButton_pingcang.setText(_translate("Form", "平仓", None))
        self.radioButton_pingjin.setText(_translate("Form", "平今", None))
        self.radioButton_mairu.setText(_translate("Form", "买入", None))
        self.label_xiadanjiage.setText(_translate("Form", "价格", None))
        self.pushButton_xiadantiaocang.setText(_translate("Form", "调仓", None))
        self.pushButton_xiandan.setText(_translate("Form", "下单", None))
        self.pushButton_xiadanquxiao.setText(_translate("Form", "取消", None))
        self.label_pankouguadansell.setText(_translate("Form", "卖 82990 / 3", None))
        self.label_dietingjia.setText(_translate("Form", "↓88020", None))
        self.label_zuidashoushu.setText(_translate("Form", "≤0", None))
        self.label_zhangtingjia.setText(_translate("Form", "↑88020", None))
        self.label_pankouguadanbuy.setText(_translate("Form", "买 82970 / 20", None))
        self.checkBox_taoli.setText(_translate("Form", "套利", None))
        self.checkBox_baozhi.setText(_translate("Form", "保值", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

