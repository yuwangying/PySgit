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

    # 设置列宽自适应
    def slot_set_resizeColumnsToContents(self):
        # if self.__set_resizeColumnsToContents_flags is False:  # not self.__set_resizeColumnsToContents_flags:
        self.__QOrderWidget.tableView_trade.resizeColumnsToContents()  # tableView列宽自动适应
        # self.__QAccountWidget.tableView_Trade_Args.resizeRowsToContents()  # tableView行高自动适应
        self.__set_resizeColumnsToContents_flags = True  # 设置过列宽标志位为True
