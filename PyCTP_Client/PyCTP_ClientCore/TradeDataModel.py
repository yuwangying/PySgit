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
    def __init__(self, parent, mylist, header=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        # 系统编号=OrderSysID
        header = ['期货账号', '策略编号', '合约', '买卖', '开平', '成交价格', '成交手数', '成交时间', '交易日', '投保', '报单引用', '系统编号', '成交编号', '交易所']
        self.header = header

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
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        if (index.column() == 0):
            value = self.mylist[index.row()][index.column()].text()
        else:
            value = self.mylist[index.row()][index.column()]
        if role == QtCore.Qt.EditRole:
            return value
        elif role == QtCore.Qt.DisplayRole:
            return value
        elif role == QtCore.Qt.ForegroundRole and index.column() == 1:
            return QtGui.QColor(255, 0, 0)
        elif role == QtCore.Qt.ForegroundRole and index.column() == 2:
            return QtGui.QColor(0, 255, 0)
        elif role == QtCore.Qt.FontRole and index.column() == 1:
            font = QtGui.QFont()
            font.setBold(True)
            return font
        elif role == QtCore.Qt.FontRole and index.column() == 2:
            font = QtGui.QFont()
            font.setBold(True)
            return font
        elif role == QtCore.Qt.TextAlignmentRole and index.column() == 1:
            return QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.TextAlignmentRole and index.column() == 2:
            return QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.CheckStateRole:
            if index.column() == 0:
                # print(">>> data() row,col = %d, %d" % (index.row(), index.column()))
                if self.mylist[index.row()][index.column()].isChecked():
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if (col < 14):
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
        if index.column() == 0:
            # return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsUserCheckable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        # print(">>> setData() role = ", role)
        # print(">>> setData() index.column() = ", index.column())
        # print(">>> setData() value = ", value)
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            print(">>> setData() role = ", role)
            print(">>> setData() index.column() = ", index.column())
            if value == QtCore.Qt.Checked:
                self.mylist[index.row()][index.column()].setChecked(True)
                self.mylist[index.row()][index.column()].setText("开")
                # if studentInfos.size() > index.row():
                #     emit StudentInfoIsChecked(studentInfos[index.row()])
            else:
                self.mylist[index.row()][index.column()].setChecked(False)
                self.mylist[index.row()][index.column()].setText("关")
        elif role == QtCore.Qt.BackgroundRole and index.column() == 1:
            return QtGui.QColor(255, 0, 0)
        else:
            print(">>> setData() role = ", role)
            print(">>> setData() index.column() = ", index.column())
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        print(">>> setData() index.row = ", index.row())
        print(">>> setData() index.column = ", index.column())
        self.dataChanged.emit(index, index)
        return True



if __name__ == '__main__':
    app = QApplication([])
    # you could process a CSV file to create this data
    header = ['开关', '只平', '期货账号', '策略编号', '交易合约', '总持仓', '买持仓', '卖持仓', '持仓盈亏', '平仓盈亏', '手续费', '净盈亏', '成交量', '成交金额', 'A成交率', 'B成交率', '交易模型', '下单算法']
    checkbox1 = QtGui.QCheckBox("关")
    checkbox1.setChecked(True)
    dataList = [
        [checkbox1, 0, '058176', '02', 'cu1705,cu1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '063802', '03', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '058176', '04', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '058176', '05', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '063802', '06', 'ru1705,ru1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '801867', '07', 'ni1705,ni1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '058176', '08', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '094969', '09', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
        [checkbox1, 0, '801867', '10', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01']
    ]

    win = MyWindow(dataList, header)
    win.show()

    # win.table_model.setDataList(dataList)
    # timer = threading.Timer(10, timer_func, (win, dataList2))
    # timer.start()
    app.exec_()