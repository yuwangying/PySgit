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
from PyQt4 import QtGui, QtCore
# from time import time
# import threading
# from PyQt4.QtGui import *


class OrderDataModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """

    def __init__(self, parent=None, mylist=[], header=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        header = ['期货账号', '策略编号', '合约', '买卖', '开平', '报单价格', '报单手数', '报单时间', '投保', '报单引用', '系统编号', '交易所']  # 12个
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
        # elif role == QtCore.Qt.ForegroundRole and index.column() == 2:
        #     return QtGui.QColor(0, 255, 0)
        # elif role == QtCore.Qt.FontRole and index.column() == 1:
        #     font = QtGui.QFont()
        #     font.setBold(True)
        #     return font
        # elif role == QtCore.Qt.FontRole and index.column() == 2:
        #     font = QtGui.QFont()
        #     font.setBold(True)
        #     return font
        # elif role == QtCore.Qt.TextAlignmentRole and index.column() == 3:
        #     return QtCore.Qt.AlignCenter
        # elif role == QtCore.Qt.TextAlignmentRole and index.column() == 2:
        #     return QtCore.Qt.AlignCenter

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
        # print(">>> setData() index.row = ", index.row())
        # print(">>> setData() index.column = ", index.column())
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
        self.__QOrderWidget.update_order_data_Filter()

    # 更新tableView，根据界面combBox组件的user_id、strategy_id来决定是否更新
    def update_data(self):
        user_id = self.__QOrderWidget.comboBox_account_id.currentText()
        if user_id == '':
            print(">>>OrderDataModel.update_data() 不需要更新的user_id =", user_id, type(user_id))
            return
        # strategy_id = self.__QOrderWidget.comboBox_strategy_id.currentText()
        # print(">>>OrderDataModel.update_data() 需要更新的user_id =", user_id, type(user_id), "strategy_id =", strategy_id, type(strategy_id))
        list_update_data = self.__dict_origin_data[user_id]
        self.slot_set_data_list(list_update_data)

    # # 设置列宽自适应
    # def slot_set_resizeColumnsToContents(self):
    #     # if self.__set_resizeColumnsToContents_flags is False:  # not self.__set_resizeColumnsToContents_flags:
    #     self.__QOrderWidget.tableView_order.resizeColumnsToContents()  # tableView列宽自动适应
    #     # self.__QAccountWidget.tableView_Trade_Args.resizeRowsToContents()  # tableView行高自动适应
    #     self.__set_resizeColumnsToContents_flags = True  # 设置过列宽标志位为True

    # 接收历史数据，形参{'801867': [order数据]}
    def slot_receive_previous_data_order(self, dict_input):
        for user_id in dict_input:
            self.__dict_origin_data[user_id] = list()  # 初始化结构体
            # print(">>>OrderDataModel.slot_receive_previous_data_order() user_id =", user_id, "dict_input['user_id'] 长度=", len(dict_input[user_id]))
            for dict_order in dict_input[user_id]:
                list_order = self.select_element_order(dict_order)  # 将原始回调数据结构dict转换为数据模型需要的结构list
                self.__dict_origin_data[user_id].insert(0, list_order)  # 最新的数据插入到list的0位置
        # print(">>>OrderDataModel.slot_receive_previous_data_order() self.__dict_origin_data[user_id] 长度=", len(self.__dict_origin_data[user_id]))
        self.update_data()  # 更新界面

    # 接收最新的回调数据，形参dict,order结构体
    def slot_receive_last_data_order(self, dict_input):
        # print(">>>OrderDataModel.slot_receive_last_data_order() dict_input =", dict_input)
        user_id = dict_input['UserID']
        list_order = self.select_element_order(dict_input)
        # print(">>>OrderDataModel.slot_receive_last_data_order() list_order =", list_order)
        for i in self.__dict_origin_data:
            # i是dict的keys，值为原始期货账号；user_id为order回调中的结构体期货账号，可能为***或***01或***02
            if i in user_id:
                self.__dict_origin_data[i].insert(0, list_order)  # 最新的数据插入到list的0位置
                # print(">>>OrderDataModel.slot_receive_last_data_order() if i in user_id")
                break
        self.update_data()  # 更新界面

    # 从dict结构体里面删选出部分元素组成list目标结构体
    def select_element_order(self, order):
        if order['Direction'] == '0':
            Direction = '买    '
        elif order['Direction'] == '1':
            Direction = '    卖'
        if order['CombOffsetFlag'] == '0':
            CombOffsetFlag = '开仓'
        elif order['CombOffsetFlag'] == '1':
            CombOffsetFlag = '平仓'
        elif order['CombOffsetFlag'] == '3':
            CombOffsetFlag = '平今'
        elif order['CombOffsetFlag'] == '4':
            CombOffsetFlag = '平昨'
        else:
            CombOffsetFlag = '未知'

        if order['CombHedgeFlag'] == '1':
            CombHedgeFlag = '投机'
        elif order['CombHedgeFlag'] == '2':
            CombHedgeFlag = '套利'
        elif order['CombHedgeFlag'] == '3':
            CombHedgeFlag = '套保'

        list_output = [
            order['UserID'],  # 期货账号
            order['StrategyID'],  # 策略编号
            order['InstrumentID'],  # 合约
            Direction,  # 买卖
            CombOffsetFlag,  # 开平
            order['LimitPrice'],  # 报单价格
            order['VolumeTotalOriginal'],  # 报单手数
            order['InsertTime'],  # 报单时间
            CombHedgeFlag,  # 投保
            order['OrderRef'],  # 报单引用
            order['OrderSysID'],  # 报单编号
            order['ExchangeID']  # 交易所
        ]
        return list_output
