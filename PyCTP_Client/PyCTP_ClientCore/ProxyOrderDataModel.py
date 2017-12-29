from PyQt4 import QtGui, QtCore
# import operator  # used for sorting
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from time import time
# import threading

class ProxyOrderDataModel(QtGui.QSortFilterProxyModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent=None):
        # QSortFilterProxyModel.__init__(self, parent)
        super(ProxyOrderDataModel, self).__init__(parent)
        self.strategy_id = ""
        self.user_id = ""

    def setStrategyIDFilter(self, strategy_id):
        # print(">>>ProxyOrderDataModel.setStrategyIDFilter() strategy_id =", strategy_id)
        if self.strategy_id != strategy_id:
            self.strategy_id = strategy_id
        self.invalidateFilter()

    def setUserIDFilter(self, user_id):
        # print(">>>ProxyOrderDataModel.setUserIDFilter() user_id =", user_id)
        if self.user_id != user_id:
            self.user_id = user_id
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        index_UserID = self.sourceModel().index(source_row, 0, source_parent)
        index_StrategyID = self.sourceModel().index(source_row, 1, source_parent)
        if (self.sourceModel().data(index_UserID, QtCore.Qt.DisplayRole) == self.user_id and self.sourceModel().data(index_StrategyID, QtCore.Qt.DisplayRole) == self.strategy_id)\
                or self.strategy_id == "所有":
            return True
        else:
            return False

    def set_QOrderWidget(self, obj):
        self.__QOrderWidget = obj

    def set_OrderDataModel(self, obj):
        self.__OrderDataModel = obj

    def set_TradeDataModel(self, obj):
        self.__OrderDataModel = obj

    def set_tableView_order(self, obj):
        self.tableView_order = obj

    def set_tableView_trade(self, obj):
        self.tableView_trade = obj