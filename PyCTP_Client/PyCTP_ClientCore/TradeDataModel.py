''' pqt_tableview3.py
explore PyQT's QTableView Model
using QAbstractTableModel to present tabular data
allow table sorting by clicking on the header title

used the Anaconda package (comes with PyQt4) on OS X
(dns)
'''

#coding=utf-8

import operator  # used for sorting
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from time import time
import threading


class TradeDataModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """

    def __init__(self, parent=None, mylist=[], header=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        header = ['期货账号', '策略编号', '合约', '买卖', '开平', '成交价格', '成交手数', '成交时间', '交易日', '投保', '报单引用', '系统编号', '成交编号', '交易所']  # 14个
        self.header = header
        self.__set_resizeColumnsToContents_flags = False  # 设置过列宽标志位为False
        # tableView_order的 {'801867': [order数据], '期货账户2': [order数据], '期货账户3': [order数据]}
        self.__dict_origin_data = dict()

    def set_QOrderWidget(self, obj):
        self.__QOrderWidget = obj

    def setDataList(self, mylist):
        self.mylist = mylist
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def rowCount(self, parent):
        # print("rowCount")
        return len(self.mylist)

    def columnCount(self, parent):
        # print("columnCount")
        if len(self.mylist) == 0:
            return 0
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        # if (index.column() == 0):
        #     value = self.mylist[index.row()][index.column()].text()
        # else:
        #     value = self.mylist[index.row()][index.column()]

        # print(">>>TradeDataModel.data() index.row() =", index.row())
        # print(">>>TradeDataModel.data() index.column() =", index.column())
        value = self.mylist[index.row()][index.column()]

        if role == QtCore.Qt.EditRole:
            return value
        elif role == QtCore.Qt.DisplayRole:
            return value
        elif role == QtCore.Qt.ForegroundRole and index.column() == 3:
            if value == '买    ':
                return QtGui.QColor(204, 51, 102)
            elif value == '    卖':
                return QtGui.QColor(51, 153, 102)
        elif role == QtCore.Qt.ForegroundRole and index.column() == 4:
            if value == '开仓':
                return QtGui.QColor(204, 51, 102)
            elif value != '开仓':
                return QtGui.QColor(51, 153, 102)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if (col < self.columnCount(0)):
                return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        # print(">>> sort() col = ", col)
        if col != 0:
            self.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
            if order == Qt.DescendingOrder:
                self.mylist.reverse()
            self.emit(SIGNAL("layoutChanged()"))

    def flags(self, index):
        if not index.isValid():
            return None
        # print(">>> flags() index.column() = ", index.column())
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        # print(">>> setData() role = ", role)
        # print(">>> setData() index.column() = ", index.column())
        # print(">>> setData() value = ", value)
        if role == QtCore.Qt.BackgroundRole and index.column() == 1:
            return QtGui.QColor(255, 0, 0)
        else:
            print(">>> setData() role = ", role)
            print(">>> setData() index.column() = ", index.column())
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        print(">>> setData() index.row = ", index.row())
        print(">>> setData() index.column = ", index.column())
        self.dataChanged.emit(index, index)
        return True

    # 更新tableView
    def slot_set_data_list(self, data_list):
        self.mylist = data_list
        self.layoutAboutToBeChanged.emit()  # 布局准备信号
        self.layoutChanged.emit()  # 布局执行信号
        t1 = self.index(0, 0)  # 左上角
        t2 = self.index(self.rowCount(0), self.columnCount(0))  # 右下角
        self.dataChanged.emit(t1, t2)
        self.__QOrderWidget.update_trade_data_Filter()
        # self.__QOrderWidget.tableView_trade.resizeColumnsToContents()  # tableView列宽自动适应

    # 更新tableView，根据界面combBox组件的user_id、strategy_id来决定是否更新
    def update_data(self):
        user_id = self.__QOrderWidget.comboBox_account_id.currentText()
        if user_id == '':
            print(">>>TradeDataModel.update_data() 不需要更新的user_id =", user_id, type(user_id))
            return
        strategy_id = self.__QOrderWidget.comboBox_strategy_id.currentText()
        print(">>>TradeDataModel.update_data() 需要更新的user_id =", user_id, type(user_id), "strategy_id =", strategy_id, type(strategy_id))
        list_update_data = self.__dict_origin_data[user_id]
        self.slot_set_data_list(list_update_data)

    # 接收历史数据，形参{'801867': [trade数据]}
    def slot_receive_previous_data_trade(self, dict_input):
        for user_id in dict_input:
            print(">>>TradeDataModel.slot_receive_previous_data_trade() user_id =", user_id, "dict_input['user_id'] 长度=",
                  len(dict_input[user_id]))
            self.__dict_origin_data[user_id] = list()  # 初始化结构体
            for dict_trade in dict_input[user_id]:
                list_trade = self.select_element_trade(dict_trade)  # 将原始回调数据结构dict转换为数据模型需要的结构list
                self.__dict_origin_data[user_id].insert(0, list_trade)  # 最新的数据插入到list的0位置
        print(">>>TradeDataModel.slot_receive_previous_data_trade() self.__dict_origin_data[user_id] 长度=", len(self.__dict_origin_data[user_id]))
        self.update_data()  # 更新界面

    # 接收最新的回调数据，形参{'801867': [order数据]}
    def slot_receive_last_data_trade(self, dict_input):
        # print(">>>TradeDataModel.slot_receive_last_data_trade() dict_input =", dict_input)
        user_id = dict_input['UserID']
        list_trade = self.select_element_trade(dict_input)
        self.__dict_origin_data[user_id].insert(0, list_trade)  # 最新的数据插入到list的0位置
        self.update_data()  # 更新界面

    # 从dict结构体里面删选出部分元素组成list目标结构体
    def select_element_trade(self, trade):
        if trade['Direction'] == '0':
            Direction = '买    '
        elif trade['Direction'] == '1':
            Direction = '    卖'

        if trade['OffsetFlag'] == '0':
            OffsetFlag = '开仓'
        elif trade['OffsetFlag'] == '1':
            OffsetFlag = '平仓'
        elif trade['OffsetFlag'] == '3':
            OffsetFlag = '平今'
        elif trade['OffsetFlag'] == '4':
            OffsetFlag = '平昨'
        else:
            OffsetFlag = '未知'

        if trade['HedgeFlag'] == '1':
            HedgeFlag = '投机'
        elif trade['HedgeFlag'] == '2':
            HedgeFlag = '套利'
        elif trade['HedgeFlag'] == '3':
            HedgeFlag = '保值'

        list_output = [
            trade['UserID'],  # 期货账号
            trade['StrategyID'],  # 策略编号
            trade['InstrumentID'],  # 合约
            Direction,  # 买卖
            OffsetFlag,  # 开平
            trade['Price'],  # 成交价格
            trade['Volume'],  # 成交手数
            trade['TradeTime'],  # 成交时间
            trade['TradingDay'],  # 交易日
            HedgeFlag,  # 投保
            trade['OrderRef'],  # 报单引用
            trade['OrderSysID'],  # 系统编号
            trade['TradeID'],  # 成交编号
            trade['ExchangeID']  # 交易所
        ]
        return list_output

    # 设置列宽自适应
    # def slot_set_resizeColumnsToContents(self):
    #     # if self.__set_resizeColumnsToContents_flags is False:  # not self.__set_resizeColumnsToContents_flags:
    #     self.__QOrderWidget.tableView_trade.resizeColumnsToContents()  # tableView列宽自动适应
    #     # self.__QAccountWidget.tableView_Trade_Args.resizeRowsToContents()  # tableView行高自动适应
    #     self.__set_resizeColumnsToContents_flags = True  # 设置过列宽标志位为True
