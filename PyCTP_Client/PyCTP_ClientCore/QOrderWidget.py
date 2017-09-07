# -*- coding: utf-8 -*-

"""
Module implementing QOrderWidget.
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QModelIndex, QPoint
from Ui_QOrderWidget import Ui_Form
import ProxyOrderDataModel
import OrderDataModel
import TradeDataModel
import copy


class QOrderWidget(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(QOrderWidget, self).__init__(parent)
        self.setupUi(self)

        # 结束内置的信号槽绑定
        # self.comboBox_strategy_id.clear.disconnect(self.comboBox_strategy_id.currentIndexChanged)
        # self.comboBox_strategy_id.insertItems.disconnect(self.comboBox_strategy_id.currentIndexChanged)

        self.init_varable()  # 初始化变量
        
        # 显示order结构体的viewTable
        self.order_data_model = OrderDataModel.OrderDataModel(parent=self)
        self.order_data_model.set_QOrderWidget(self)
        self.__proxy_order_data_model = ProxyOrderDataModel.ProxyOrderDataModel()
        self.__proxy_order_data_model.set_tableView_order(self.tableView_order)
        self.__proxy_order_data_model.setSourceModel(self.order_data_model)
        self.tableView_order.setModel(self.__proxy_order_data_model)
        self.order_data_model.set_QOrderWidget(self)

        # 显示trade结构体的viewTable
        self.trade_data_model = TradeDataModel.TradeDataModel(parent=self)
        self.trade_data_model.set_QOrderWidget(self)
        self.__proxy_trade_data_model = ProxyOrderDataModel.ProxyOrderDataModel()
        self.__proxy_order_data_model.set_tableView_trade(self.tableView_trade)
        self.__proxy_trade_data_model.setSourceModel(self.trade_data_model)
        self.tableView_trade.setModel(self.__proxy_trade_data_model)
        self.trade_data_model.set_QOrderWidget(self)

        self.horizontalHeader_order = self.tableView_order.horizontalHeader()
        self.horizontalHeader_order.sectionClicked.connect(self.on_order_view_horizontalHeader_sectionClicked)

        self.horizontalHeader_trade = self.tableView_trade.horizontalHeader()
        self.horizontalHeader_trade.sectionClicked.connect(self.on_trade_view_horizontalHeader_sectionClicked)

    # @QtCore.pyqtSlot(int)
    def on_order_view_horizontalHeader_sectionClicked(self, logicalIndex):
        # self.logicalIndex = logicalIndex
        self.order_menuValues = QtGui.QMenu(self)
        # self.signalMapper = QtCore.QSignalMapper(self)

        # self.comboBox.blockSignals(True)
        # self.comboBox.setCurrentIndex(self.logicalIndex)
        # self.comboBox.blockSignals(True)
        #
        # valuesUnique = [self.model.item(row, self.logicalIndex).text()
        #                 for row in range(self.model.rowCount())
        #                 ]

        actionAll = QtGui.QAction("自适应列宽", self)
        actionAll.triggered.connect(self.on_order_triggered)
        # actionAll.triggered.connect(self.tableView_order.resizeColumnsToContents)
        self.order_menuValues.addAction(actionAll)
        # self.menuValues.addSeparator()

        # for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
        #     action = QtGui.QAction(actionName, self)
        #     self.signalMapper.setMapping(action, actionNumber)
        #     action.triggered.connect(self.signalMapper.map)
        #     self.menuValues.addAction(action)
        #
        # self.signalMapper.mapped.connect(self.on_signalMapper_mapped)

        headerPos = self.tableView_order.mapToGlobal(self.horizontalHeader_order.pos())
        posY = headerPos.y() + self.horizontalHeader_order.height()
        posX = headerPos.x() + self.horizontalHeader_order.sectionPosition(logicalIndex)
        self.order_menuValues.exec_(QtCore.QPoint(posX, posY))

    def on_order_triggered(self):
        self.tableView_order.resizeColumnsToContents()

    # @QtCore.pyqtSlot(int)
    def on_trade_view_horizontalHeader_sectionClicked(self, logicalIndex):
        # self.logicalIndex = logicalIndex
        self.trade_menuValues = QtGui.QMenu(self)
        # self.signalMapper = QtCore.QSignalMapper(self)

        # self.comboBox.blockSignals(True)
        # self.comboBox.setCurrentIndex(self.logicalIndex)
        # self.comboBox.blockSignals(True)
        #
        # valuesUnique = [self.model.item(row, self.logicalIndex).text()
        #                 for row in range(self.model.rowCount())
        #                 ]

        actionAll = QtGui.QAction("自适应列宽", self)
        actionAll.triggered.connect(self.on_trade_triggered)
        # actionAll.triggered.connect(self.tableView_trade.resizeColumnsToContents)
        self.trade_menuValues.addAction(actionAll)
        # self.menuValues.addSeparator()

        # for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
        #     action = QtGui.QAction(actionName, self)
        #     self.signalMapper.setMapping(action, actionNumber)
        #     action.triggered.connect(self.signalMapper.map)
        #     self.menuValues.addAction(action)
        #
        # self.signalMapper.mapped.connect(self.on_signalMapper_mapped)

        headerPos = self.tableView_trade.mapToGlobal(self.horizontalHeader_trade.pos())
        posY = headerPos.y() + self.horizontalHeader_trade.height()
        posX = headerPos.x() + self.horizontalHeader_trade.sectionPosition(logicalIndex)
        self.trade_menuValues.exec_(QtCore.QPoint(posX, posY))

    def on_trade_triggered(self):
        self.tableView_trade.resizeColumnsToContents()

    def init_varable(self):
        self.__already_init_comboBox_account_id = False  # 已经设置过期货账号的combBox菜单
        self.last_combBox_strategy_id = "所有"  # 策略编号combBox中最近一次显示的策略
        self.__add_all_strategy_in_menu = False  # 策略的combBox中已经插入过“所有”
        # self.__flag_list_menu_modify = False  # 策略的combBox菜单长度有变化
        self.__last_len_list_menu = 0  # 策略combBox菜单长度初始值

    def set_SocketManager(self, obj_SocketManager):
        self.__set_socket_manager = True
        self.__socket_manager = obj_SocketManager
        # 信号槽连接：追进程收到user进程的order数据 -> 界面更新数据
        self.__socket_manager.signal_set_data_list_order.connect(self.order_data_model.slot_set_data_list)
        # 信号槽连接：追进程收到user进程的trade数据 -> 界面更新数据
        self.__socket_manager.signal_set_data_list_trade.connect(self.trade_data_model.slot_set_data_list)
        # 信号槽连接：socket_manager发送设置自适应列宽信号 -> order_data_model设置自适应列宽
        # self.__socket_manager.signal_set_resizeColumnsToContents_order.connect(self.order_data_model.slot_set_resizeColumnsToContents)
        # 信号槽连接：socket_manager发送设置自适应列宽信号 -> trade_data_model设置自适应列宽
        # self.__socket_manager.signal_set_resizeColumnsToContents_trade.connect(self.trade_data_model.slot_set_resizeColumnsToContents)
        # 信号槽连接：socket_manager发送dcit_user_strategy_tree -> QOrderWidget设置期货账户和策略的combBox菜单
        self.__socket_manager.signal_set_user_strategy_tree.connect(self.slot_set_combBox_user_strategy)

    # 初始化comboBox可选项：期货账号
    def init_comboBox_account_id(self, list_input):
        if self.__already_init_comboBox_account_id is False:  # 未设置过
            self.comboBox_account_id.clear()
            list_input.sort()  # 排序：升序
            self.comboBox_account_id.insertItems(0, list_input)
            self.comboBox_account_id.setCurrentIndex(0)
            # user_id = self.comboBox_account_id.currentText()
            # list_strategy = self.__dict_user_strategy_tree[user_id]
            # self.init_comboBox_strategy_id(list_strategy)
            self.__already_init_comboBox_account_id = True

    # 初始化comboBox可选项：策略编号，仅考虑期货账户不变话，策略增删改
    def init_comboBox_strategy_id(self, list_input):
        list_menu = copy.deepcopy(list_input)
        list_menu.sort()
        list_menu.insert(0, "所有")  # 在第一的位置插入"所有"
        #
        # if len(list_menu) != self.__last_len_list_menu:  #
        #     self.__flag_list_menu_modify = True  # 策略的combBox菜单长度有变化
        # else:
        #     self.__flag_list_menu_modify = False  # 策略的combBox菜单长度有变化

        self.comboBox_strategy_id.blockSignals(True)
        self.comboBox_strategy_id.clear()
        self.comboBox_strategy_id.insertItems(0, list_menu)
        self.comboBox_strategy_id.blockSignals(False)
        # 最近一次显示的策略编号没有被删除，继续显示该策略编号
        if self.last_combBox_strategy_id in list_menu:
            print("if self.last_combBox_strategy_id in list_menu: self.last_combBox_strategy_id =", self.last_combBox_strategy_id)
            set_index = self.comboBox_strategy_id.findText(self.last_combBox_strategy_id)
            self.comboBox_strategy_id.setCurrentIndex(set_index)
        else:
            print("! if self.last_combBox_strategy_id in list_menu: self.last_combBox_strategy_id =", self.last_combBox_strategy_id)
            self.comboBox_strategy_id.setCurrentIndex(0)
        # self.last_combBox_strategy_id = self.comboBox_strategy_id.currentText()  # 保存最后一次显示的策略编号
        print(">>>QOrderWidget.init_comboBox_strategy_id() self.last_combBox_strategy_id =", self.last_combBox_strategy_id)

        self.__last_len_list_menu = len(list_menu)  #

    # 设置user、strategy的combBox中可选菜单
    def slot_set_combBox_user_strategy(self, dict_input):
        self.__dict_user_strategy_tree = dict_input
        list_user_id = list()
        for user_id in self.__dict_user_strategy_tree:
            list_user_id.append(user_id)
        self.init_comboBox_account_id(list_user_id)  # 设置期货账号combBox菜单
        current_user_id = self.comboBox_account_id.currentText()  # 期货账号combBox当前显示的user_id
        list_strategy_id = self.__dict_user_strategy_tree[current_user_id]
        print(">>>QOrderWidget.slot_set_combBox_user_strategy() list_strategy_id =", list_strategy_id)
        self.init_comboBox_strategy_id(list_strategy_id)

    # 更新过滤条件
    def update_order_data_Filter(self):
        user_id = self.comboBox_account_id.currentText()
        strategy_id = self.comboBox_strategy_id.currentText()
        self.__proxy_order_data_model.setUserIDFilter(user_id)
        self.__proxy_order_data_model.setStrategyIDFilter(strategy_id)

    # 更新过滤条件
    def update_trade_data_Filter(self):
        user_id = self.comboBox_account_id.currentText()
        strategy_id = self.comboBox_strategy_id.currentText()
        self.__proxy_trade_data_model.setUserIDFilter(user_id)
        self.__proxy_trade_data_model.setStrategyIDFilter(strategy_id)

    @pyqtSlot(str)
    def on_lineEdit_heyue_textChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(str)
    def on_lineEdit_heyue_textEdited(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_kaicang_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_kaicang_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_kaicang_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_maichu_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_maichu_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_maichu_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_pingcang_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_pingcang_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_pingcang_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_spinBox_shoushu_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(str)
    def on_spinBox_shoushu_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_pingjin_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_pingjin_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_pingjin_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_mairu_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_mairu_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_radioButton_mairu_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(float)
    def on_doubleSpinBox_xiadanjiage_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type float
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(str)
    def on_doubleSpinBox_xiadanjiage_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadantiaocang_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadantiaocang_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadantiaocang_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiandan_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiandan_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiandan_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadanquxiao_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadanquxiao_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_xiadanquxiao_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_checkBox_taoli_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBox_taoli_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_checkBox_taoli_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_checkBox_taoli_stateChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_checkBox_baozhi_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBox_baozhi_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(bool)
    def on_checkBox_baozhi_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_checkBox_baozhi_stateChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_comboBox_account_id_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(str)
    def on_comboBox_account_id_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_comboBox_account_id_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    @pyqtSlot(str)
    def on_comboBox_account_id_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_comboBox_strategy_id_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(str)
    def on_comboBox_strategy_id_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(int)
    def on_comboBox_strategy_id_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        self.last_combBox_strategy_id = self.comboBox_strategy_id.currentText()
        user_id = self.comboBox_account_id.currentText()
        self.update_order_data_Filter()  # 更新界面过滤条件
        self.update_trade_data_Filter()  # 更新界面过滤条件
        # if self.__flag_list_menu_modify is False:
        #     self.last_combBox_strategy_id = self.comboBox_strategy_id.currentText()
        #     print(">>>QOrderWidget.on_comboBox_strategy_id_currentIndexChanged() 用户操作 self.last_combBox_strategy_id", self.last_combBox_strategy_id)
        # else:
        #     self.__flag_list_menu_modify = False
        #     print(">>>QOrderWidget.on_comboBox_strategy_id_currentIndexChanged() 非用户操作 self.last_combBox_strategy_id", self.last_combBox_strategy_id)


    # @pyqtSlot(str)
    # def on_comboBox_strategy_id_currentIndexChanged(self, p0):
    #     """
    #     Slot documentation goes here.
    #
    #     @param p0 DESCRIPTION
    #     @type str
    #     """
    #     # TODO: not implemented yet
    #     self.last_combBox_strategy_id = self.comboBox_strategy_id.currentText()
    #     print(">>>QOrderWidget.on_comboBox_strategy_id_currentIndexChanged() p0 self.last_combBox_strategy_id", self.last_combBox_strategy_id)

    
    @pyqtSlot(QPoint)
    def on_tableView_all_orders_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        
        @param pos DESCRIPTION
        @type QPoint
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_all_orders_pressed(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_all_orders_clicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_all_orders_doubleClicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_all_orders_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_all_orders_entered(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QPoint)
    def on_tableView_trade_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        
        @param pos DESCRIPTION
        @type QPoint
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_trade_pressed(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_trade_clicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_trade_doubleClicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_trade_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_trade_entered(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QPoint)
    def on_tableView_order_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        
        @param pos DESCRIPTION
        @type QPoint
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_order_pressed(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_order_clicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_order_doubleClicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_order_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
    
    @pyqtSlot(QModelIndex)
    def on_tableView_order_entered(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # TODO: not implemented yet
        pass  # raise NotImplementedError
