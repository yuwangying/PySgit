import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from QCTP import QCTP
import json
import threading
from Strategy import Strategy
from SocketManager import SocketManager
from XML_Manager import XML_Manager
from QAlertBox import QAlertBox
import QLogin
import multiprocessing
import win32api
import shutil
import datetime
# from TimerThread import TimerThread
# from multiprocessing import Process, Manager, Value, Array, Queue, Pipe
# from CTPManager import CTPManager
# from QAccountWidget import QAccountWidget
# from QNewStrategy import QNewStrategy
# from SocketManager import SocketManager
# import Utils
# import time
# from MarketManager import MarketManager
# from Trader import Trader
# from User import User
# from MessageBox import MessageBox


class ClientMain(QtCore.QObject):

    signal_send_msg = QtCore.pyqtSignal(str)  # 定义信号：发送到服务端的json格式数据
    signal_pushButton_query_strategy_setEnabled = QtCore.pyqtSignal(bool)  # 定义信号：控制查询是否可用
    signal_pushButton_set_position_setEnabled = QtCore.pyqtSignal()  # 定义信号：按钮设置为可用
    signal_UI_update_strategy = QtCore.pyqtSignal(Strategy)  # 改写，定义信号：形参为用户自定义类Strategy，界面中刷新策略
    signal_UI_insert_strategy = QtCore.pyqtSignal(Strategy)  # 改写，定义信号：形参为用户自定义类Strategy，界面中插入策略
    signal_UI_set_on_tableWidget_Trade_Args_cellClicked = QtCore.pyqtSignal(int, int)  # 改写，信号：触发鼠标点击事件
    signal_slot_output_message = QtCore.pyqtSignal(dict)  # 收到socketManager之后，发送处理消息信号

    def __init__(self, parent=None):
        super(ClientMain, self).__init__(parent)  # 显示调用父类初始化方法，使用其信号槽机制
        self.__list_QAccountWidget = list()  # 存放账户窗口
        self.__init_UI_finished = False  # 窗口创建完成
        self.__showEvent = False  # 有任何一个QAccountWidget窗口显示
        # self.signal_slot_output_message.connect(self.run)

    def set_SocketManager(self, obj_sorcket_manager):
        self.__socket_manager = obj_sorcket_manager
        # self.__socket_manager.signal_send_message.connect(self.slot_output_message)  # 绑定信号槽函数:
        # self.signal_send_msg.connect(self.__socket_manager.send_msg)  # 绑定信号槽函数

    def set_QLoginForm(self, qloginform):
        self.__q_login_form = qloginform

    def set_QCTP(self, obj_QCTP):
        self.__q_ctp = obj_QCTP

    def set_QAccountWidget(self, obj_QAccountWidget):
        self.__QAccoutWidget = obj_QAccountWidget

    def set_dict_QAccountWidget(self, dict_QAccountWidget):
        self.__dict_QAccountWidget = dict_QAccountWidget

    def set_QOrderWidget(self, obj_QOrderWidget):
        self.__QOrderWidget = obj_QOrderWidget

    def set_CTPManager(self, obj_CTPManager):
        self.__ctp_manager = obj_CTPManager

    # # 设置当前显示在最前端窗口对象为本类属性
    # def set_showQAccountWidget(self, obj_QAccountWidget):
    #     self.__showQAccountWidget = obj_QAccountWidget
    #     # 绑定信号：当前最前端窗口对象(通过信槽绑定的标志来判断，不能重复绑定信号槽)
    #     if self.__showQAccountWidget.get_signal_pushButton_set_position_setEnabled_connected() is False:
    #         self.signal_pushButton_set_position_setEnabled.connect(self.__showQAccountWidget.on_pushButton_set_position_active)  # , QtCore.Qt.UniqueConnection
    #         self.__showQAccountWidget.set_signal_pushButton_set_position_setEnabled_connected(True)  # 信号槽绑定状态设置为True
    #         # print(">>> ClientMain.set_showQAccountWidget() 绑定信号槽，widget_name=", self.__showQAccountWidget.get_widget_name())

    def get_showQAccountWidget(self):
        return self.__showQAccountWidget

    # def set_hideQAccountWidget(self, obj_QAccountWidget):
    #     self.__hideQAccountWidget = obj_QAccountWidget
    #     # 解绑信号：隐藏的窗口
    #     if self.__hideQAccountWidget.get_signal_pushButton_set_position_setEnabled_connected():
    #         self.signal_pushButton_set_position_setEnabled.disconnect(self.__hideQAccountWidget.on_pushButton_set_position_active)
    #         self.__hideQAccountWidget.set_signal_pushButton_set_position_setEnabled_connected(False)  # 信号槽绑定状态设置为False
    #         # print(">>> ClientMain.set_hideQAccountWidget() 解绑信号槽，widget_name=", self.__hideQAccountWidget.get_widget_name())

    def get_hideQAccountWidget(self):
        return self.__hideQAccountWidget

    def get_SocketManager(self):
        return self.__socket_manager

    def get_QLoginForm(self):
        return self.__q_login_form

    def get_QCTP(self):
        return self.__q_ctp

    def get_QAccoutWidget(self):
        return self.__QAccoutWidget

    def get_QOrderWidget(self):
        return self.__QOrderWidget

    def get_CTPManager(self):
        return self.__ctp_manager

    # 设置鼠标点击状态，信息包含:item所在行、item所在列、widget_name、user_id、strategy_id
    def set_clicked_status(self, in_dict):
        self.__clicked_status = in_dict

    def get_clicked_status(self):
        return self.__clicked_status

    # 显示在最前端窗口名称
    def set_show_widget_name(self, str_widget_name):
        self.__show_widget_name = str_widget_name

    def get_show_widget_name(self):
        return self.__show_widget_name

    def set_init_UI_finished(self, bool_input):
        self.__init_UI_finished = bool_input

    def get_init_UI_finished(self):
        return self.__init_UI_finished
    
    def set_trader_id(self, str_trader_id):
        self.__trader_id = str_trader_id

    def get_trader_id(self):
        return self.__trader_id

    def set_trader_name(self, str_trader_name):
        self.__trader_name = str_trader_name

    def get_trader_name(self):
        return self.__trader_name

    def set_QNewStrategy(self, obj_QNewStrategy):
        self.__q_new_strategy = obj_QNewStrategy

    def get_QNewStrategy(self):
        return self.__q_new_strategy

    # 最后新建的策略设置为其属性
    def set_obj_new_strategy(self, obj_strategy):
        self.__obj_new_strategy = obj_strategy

    def get_obj_new_strategy(self):
        return self.__obj_new_strategy

    # 是否有任何窗口showEvent
    def set_showEvent(self, bool_input):
        self.__showEvent = bool_input

    def get_showEvent(self):
        return self.__showEvent

    # 被鼠标点击的策略实例对象为该类属性，全局唯一
    def set_clicked_strategy(self, obj_strategy):
        # print(">>> ClientMain.set_clicked_strategy() user_id=", obj_strategy.get_user_id(), "strategy_id=", obj_strategy.get_strategy_id())
        self.__clicked_strategy = obj_strategy

    def get_clicked_strategy(self):
        return self.__clicked_strategy

    def set_clicked_item(self, obj_item):
        self.__clicked_item = obj_item

    def get_clicked_item(self):
        return self.__clicked_item

    def set_show_widget(self, obj_widget):
        self.__show_widget = obj_widget

    def get_show_widget(self):
        return self.__show_widget

    def set_list_QAccountWidget(self, list_obj):
        self.__list_QAccountWidget = list_obj

    def get_list_QAccountWidget(self):
        return self.__list_QAccountWidget

    """
    # 处理socket_manager发来的消息
    @QtCore.pyqtSlot(dict)
    def slot_output_message(self, buff):
        # 消息源MsgSrc值：0客户端、1服务端
        if buff['MsgSrc'] == 0:  # 由客户端发起的消息类型
            # 内核初始化未完成
            if self.__ctp_manager.get_init_finished() is False:
                if buff['MsgType'] == 1:  # 交易员登录验证，MsgType=1
                    print("ClientMain.slot_output_message() MsgType=1", buff)  # 输出错误消息
                    if buff['MsgResult'] == 0:  # 验证通过
                        # self.get_QLoginForm().label_login_error.setText(buff['MsgErrorReason'])  # 界面提示信息
                        self.get_QLoginForm().label_login_error.setText('登陆成功，初始化中...')  # 界面提示信息
                        self.__ctp_manager.set_trader_id(buff['TraderID'])  # 将TraderID设置为CTPManager的属性
                        self.__ctp_manager.set_trader_name(buff['TraderName'])  # 将TraderID设置为CTPManager的属性
                        # self.__ctp_manager.create_trader({"trader_id": buff['TraderID'], "trader_name": buff['TraderName']})
                        self.__trader_id = buff['TraderID']
                        self.__trader_name = buff['TraderName']
                        self.QryMarketInfo()  # 查询行情配置
                        # self.__socket_manager.signal_send_message.emit(self.slot_output_message)  # 绑定自定义信号槽
                    elif buff['MsgResult'] == 1:  # 验证不通过
                        self.get_QLoginForm().label_login_error.setText(buff['MsgErrorReason'])  # 界面提示错误信息
                        self.get_QLoginForm().pushButton_login.setEnabled(True)  # 登录按钮激活
                elif buff['MsgType'] == 4:  # 查询行情配置，MsgType=4
                    print("ClientMain.slot_output_message() MsgType=4", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listMarketInfo = buff['Info']  # 转存行情信息到本类的属性里
                        self.QryUserInfo()  # 查询期货账户
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        pass
                elif buff['MsgType'] == 2:  # 查询期货账户，MsgType=2
                    print("ClientMain.slot_output_message() MsgType=2", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listUserInfo = buff['Info']  # 转存期货账户信息到本类的属性里
                        self.QryAlgorithmInfo()  # 查询下单算法信息
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        pass
                elif buff['MsgType'] == 11:  # 查询下单算法编号，MsgType=11
                    print("ClientMain.slot_output_message() MsgType=11", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listAlgorithmInfo = buff['Info']  # 转存期货账户信息到本类的属性里
                        self.QryStrategyInfo()  # 查询策略信息
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        pass
                elif buff['MsgType'] == 3:  # 查询策略，MsgType=3
                    print("ClientMain.slot_output_message() MsgType=3", buff)  # 输出错误消息
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listStrategyInfo = buff['Info']  # 转存策略信息到本类的属性里
                        self.QryYesterdayPosition()
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        pass
                elif buff['MsgType'] == 10:  # 查询策略昨仓，MsgType=10
                    print("ClientMain.slot_output_message() MsgType=10", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listYesterdayPosition = buff['Info']  # 所有策略昨仓的list
                        self.__ctp_manager.set_YesterdayPosition(buff['Info'])  # 所有策略昨仓的list设置为CTPManager属性
                        if self.__ctp_manager.get_init_finished() is False:
                            self.__ctp_manager.init()  # 跳转到开始初始化程序，有CTPManager开始初始化
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        pass
            # 内核初始化完成
            elif self.__ctp_manager.get_init_finished():
                if buff['MsgType'] == 3:  # 查询策略，MsgType=3
                    print("ClientMain.slot_output_message() MsgType=3", buff)  # 输出错误消息
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.__listStrategyInfoOnce = buff['Info']  # 转存策略信息到本类的属性里(单次查询)
                        # 遍历查询到的消息结果列表
                        for i_Info in self.__listStrategyInfoOnce:
                            # 遍历策略对象列表，将服务器查询到的策略参数传递给策略，并调用set_arguments方法更新内核参数值
                            for i_strategy in self.__ctp_manager.get_list_strategy():
                                if i_Info['user_id'] == i_strategy.get_user_id() and i_Info['strategy_id'] == i_strategy.get_strategy_id():
                                    i_strategy.set_arguments(i_Info)  # 将查询参数结果设置到策略内核，所有的策略
                                    self.signal_UI_update_strategy.emit(i_strategy)  # 更新策略在界面显示，（槽绑定到所有窗口对象槽函数update_strategy）
                                    break
                        self.signal_pushButton_query_strategy_setEnabled.emit(True)  # 收到消息后将按钮激活
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=3 查询策略失败")
                elif buff['MsgType'] == 6:  # 新建策略，MsgType=6
                    print("ClientMain.slot_output_message() MsgType=6", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        self.get_CTPManager().create_strategy(buff['Info'][0])  # 内核创建策略对象
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() ", buff['MsgErrorReason'])
                elif buff['MsgType'] == 5:  # 修改策略参数，MsgType=5
                    print("ClientMain.slot_output_message() MsgType=5", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        for i_strategy in self.__ctp_manager.get_list_strategy():
                            if i_strategy.get_user_id() == buff['UserID'] \
                                    and i_strategy.get_strategy_id() == buff['StrategyID']:
                                i_strategy.set_arguments(buff['Info'][0])
                                # self.signal_UI_update_strategy.emit(i_strategy)  # 更新策略在界面显示，（槽绑定到所有窗口对象槽函数update_strategy）
                            break
                        # for i_widget in self.__list_QAccountWidget:
                        #     i_widget.update_groupBox_trade_args_for_set()  # 更新策略参数框goupBox
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=5 修改策略参数失败")
                elif buff['MsgType'] == 12:  # 修改策略持仓，MsgType=12
                    print("ClientMain.slot_output_message() MsgType=12", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        # 更新内核中的策略持仓
                        for i_strategy in self.__ctp_manager.get_list_strategy():
                            if i_strategy.get_user_id() == buff['UserID'] \
                                    and i_strategy.get_strategy_id() == buff['StrategyID']:
                                i_strategy.set_position(buff['Info'][0])
                            break
                        self.signal_pushButton_set_position_setEnabled.emit()  # 激活设置持仓按钮，禁用仓位输入框
                        pass
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=12 修改策略持仓失败")
                elif buff['MsgType'] == 7:  # 删除策略，MsgType=7
                    print("ClientMain.slot_output_message() MsgType=7", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        dict_args = {'user_id': buff['UserID'], 'strategy_id': buff['StrategyID']}
                        self.__ctp_manager.delete_strategy(dict_args)
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=7 删除策略失败")
                elif buff['MsgType'] == 13:  # 修改策略交易开关
                    print("ClientMain.slot_output_message() MsgType=13", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        for i_strategy in self.__ctp_manager.get_list_strategy():
                            if i_strategy.get_user_id() == buff['UserID'] and i_strategy.get_strategy_id() == buff['StrategyID']:
                                i_strategy.set_on_off(buff['OnOff'])  # 更新内核中策略开关
                                # self.signal_update_strategy.emit(i_strategy)  # 更新策略在界面显示
                                # self.get_clicked_item().setFlags(self.get_clicked_item().flags() ^ (QtCore.Qt.ItemIsEnabled))
                                break
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=13 修改策略交易开关失败")
                elif buff['MsgType'] == 14:  # 修改策略只平开关
                    print("ClientMain.slot_output_message() MsgType=14", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        for i_strategy in self.__ctp_manager.get_list_strategy():
                            if i_strategy.get_user_id() == buff['UserID'] and i_strategy.get_strategy_id() == buff['StrategyID']:
                                i_strategy.set_only_close(buff['OnOff'])  # 更新内核中策略只平开关
                                # self.signal_update_strategy.emit(i_strategy)  # 更新策略在界面显示
                                # self.get_clicked_item().setFlags(self.get_clicked_item().flags() ^ (QtCore.Qt.ItemIsEnabled))
                                break
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=14 修改策略只平开关失败")
                elif buff['MsgType'] == 8:  # 修改交易员开关
                    print("ClientMain.slot_output_message() MsgType=8", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        # 更新界面
                        for i_widget in self.__list_QAccountWidget:
                            if i_widget.get_widget_name() == "总账户":
                                self.get_CTPManager().set_on_off(buff['OnOff'])  # 设置内核值
                                # 界面按钮文字显示
                                # if buff['OnOff'] == 1:
                                #     i_widget.pushButton_start_strategy.setText("停止策略")
                                # elif buff['OnOff'] == 0:
                                #     i_widget.pushButton_start_strategy.setText("开始策略")
                                # i_widget.pushButton_start_strategy.setEnabled(True)  # 解禁按钮setEnabled
                                break
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=8 修改交易员开关失败")
                elif buff['MsgType'] == 9:  # 修改期货账户开关
                    print("ClientMain.slot_output_message() MsgType=9", buff)
                    if buff['MsgResult'] == 0:  # 消息结果成功
                        # 更新界面
                        for i_widget in self.__list_QAccountWidget:
                            if i_widget.get_widget_name() == buff['UserID']:
                                # 设置内核设值
                                for i_user in self.get_CTPManager().get_list_user():
                                    if i_user.get_user_id().decode() == buff['UserID']:
                                        i_user.set_on_off(buff['OnOff'])
                                # 界面按钮文字显示
                                # if buff['OnOff'] == 1:
                                #     i_widget.pushButton_start_strategy.setText("停止策略")
                                # elif buff['OnOff'] == 0:
                                #     i_widget.pushButton_start_strategy.setText("开始策略")
                                # i_widget.pushButton_start_strategy.setEnabled(True)  # 解禁按钮
                                break
                    elif buff['MsgResult'] == 1:  # 消息结果失败
                        print("ClientMain.slot_output_message() MsgType=9 修改期货账户开关失败")
        elif buff['MsgSrc'] == 1:  # 由服务端发起的消息类型
            pass
    """

    # 查询行情信息
    def QryMarketInfo(self):
        dict_QryMarketInfo = {'MsgRef': self.__socket_manager.msg_ref_add(),
                              'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
                              'MsgSrc': 0,  # 消息源，客户端0，服务端1
                              'MsgType': 4,  # 查询行情信息
                              'TraderID': self.__trader_id
                              }
        json_QryMarketInfo = json.dumps(dict_QryMarketInfo)
        self.get_SocketManager().send_msg(json_QryMarketInfo)

    # 查询期货账户
    def QryUserInfo(self):
        dict_QryUserInfo = {'MsgRef': self.__socket_manager.msg_ref_add(),
                            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
                            'MsgSrc': 0,  # 消息源，客户端0，服务端1
                            'MsgType': 2,  # 查询期货账户
                            'TraderID': self.__trader_id,
                            'UserID': ''
                            }
        json_QryUserInfo = json.dumps(dict_QryUserInfo)
        self.get_SocketManager().send_msg(json_QryUserInfo)

    # 查询下单算法
    def QryAlgorithmInfo(self):
        dict_QryAlgorithmInfo = {'MsgRef': self.__socket_manager.msg_ref_add(),
                                 'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
                                 'MsgSrc': 0,  # 消息源，客户端0，服务端1
                                 'MsgType': 11,  # 查询期货账户
                                 'TraderID': self.__trader_id,
                                 }
        json_QryAlgorithmInfo = json.dumps(dict_QryAlgorithmInfo)
        self.get_SocketManager().send_msg(json_QryAlgorithmInfo)

    # 查询策略
    def QryStrategyInfo(self, UserID="", StrategyID=""):
        dict_QryStrategyInfo = {'MsgRef': self.__socket_manager.msg_ref_add(),
                                'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
                                'MsgSrc': 0,  # 消息源，客户端0，服务端1
                                'MsgType': 3,  # 查询策略
                                'TraderID': self.__trader_id,
                                'UserID': UserID,
                                'StrategyID': StrategyID
                                }
        json_QryStrategyInfo = json.dumps(dict_QryStrategyInfo)
        # self.get_SocketManager().send_msg(json_QryStrategyInfo)
        self.signal_send_msg.emit(json_QryStrategyInfo)

    # 查询策略昨仓
    def QryYesterdayPosition(self):
        dict_QryYesterdayPosition = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 10,  # 查询策略昨仓
            'TraderID': self.__ctp_manager.get_trader_id(),
            'UserID': ""  # self.__user_id, 键值为空时查询所有UserID的策略
            }
        json_QryYesterdayPosition = json.dumps(dict_QryYesterdayPosition)
        self.get_SocketManager().send_msg(json_QryYesterdayPosition)

    # 新建策略
    def CreateStrategy(self, dict_info):
        dict_CreateStrategy = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 6,  # 新建策略
            'TraderID': self.get_trader_id(),
            'UserID': dict_info['user_id'],
            'Info': [dict_info]
        }
        json_CreateStrategy = json.dumps(dict_CreateStrategy)
        # self.get_SocketManager().send_msg(json_CreateStrategy)
        self.signal_send_msg.emit(json_CreateStrategy)

    # 交易员的交易开关
    def SendTraderOnOff(self, dict_info):
        dict_CreateStrategy = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 6,  # 期货账户的交易开关
            'TraderID': self.get_trader_id(),
            'UserID': dict_info['user_id'],
            'Info': [dict_info]
        }
        json_CreateStrategy = json.dumps(dict_CreateStrategy)
        # self.get_SocketManager().send_msg(json_CreateStrategy)
        self.signal_send_msg.emit(json_CreateStrategy)

    # 期货账户的交易开关
    def SendUserOnOff(self, dict_info):
        dict_CreateStrategy = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 6,  # 期货账户的交易开关
            'TraderID': self.get_trader_id(),
            'UserID': dict_info['user_id'],
            'Info': [dict_info]
        }
        json_CreateStrategy = json.dumps(dict_CreateStrategy)
        # self.get_SocketManager().send_msg(json_CreateStrategy)
        self.signal_send_msg.emit(json_CreateStrategy)

    # 策略交易开关
    def SendStrategyOnOff(self, dict_args):
        dict_SendStrategyOnOff = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 13,  # 策略交易开关
            'TraderID': self.get_trader_id(),
            'UserID': dict_args['user_id'],
            'StrategyID': dict_args['strategy_id'],
            'OnOff': dict_args['on_off']
        }
        json_SendStrategyOnOff = json.dumps(dict_SendStrategyOnOff)
        self.signal_send_msg.emit(json_SendStrategyOnOff)

    # 策略只平开关
    def SendStrategyOnlyClose(self, dict_args):
        dict_StrategyOnlyClose = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 14,  # 策略只平开关
            'TraderID': self.get_trader_id(),
            'UserID': dict_args['user_id'],
            'StrategyID': dict_args['strategy_id'],
            'OnOff': dict_args['on_off']
        }
        json_StrategyOnlyClose = json.dumps(dict_StrategyOnlyClose)
        self.signal_send_msg.emit(json_StrategyOnlyClose)

    # 交易员交易开关
    def SendTraderOnoff(self, dict_args):
        dict_TraderOnoff = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 8,  # 交易员交易开关
            'TraderID': self.get_trader_id(),
            'OnOff': dict_args['on_off']
        }
        json_TraderOnoff = json.dumps(dict_TraderOnoff)
        self.signal_send_msg.emit(json_TraderOnoff)

    # 期货账户交易开关
    def SendUserOnoff(self, dict_args):
        dict_UserOnoff = {
            'MsgRef': self.__socket_manager.msg_ref_add(),
            'MsgSendFlag': 0,  # 发送标志，客户端发出0，服务端发出1
            'MsgSrc': 0,  # 消息源，客户端0，服务端1
            'MsgType': 9,  # 期货账户交易开关
            'TraderID': self.get_trader_id(),
            'UserID': dict_args['user_id'],
            'OnOff': dict_args['on_off']
        }
        json_UserOnoff = json.dumps(dict_UserOnoff)
        self.signal_send_msg.emit(json_UserOnoff)
        
    # def update_strategy(self, obj_strategy):
    #     pass

    # 所有窗口中更新单个策略的参数显示，一个策略对应两个窗口（总账户窗口、策略所属的单账户窗口）
    def update_tableWidget_Trade_Args(self, obj_strategy):
        # 遍历窗口
        for i_widget in self.__list_QAccountWidget:
            if i_widget.get_widget_name() in [obj_strategy.get_user_id(), "所有账户"]:
                for i_row in range(self.tableWidget_Trade_Args.rowCount()):  # 遍历界面的策略参数表
                    # 找到行的user_id、strategy_id与策略实例一致
                    if i_widget.tableWidget_Trade_Args.item(i_row, 2).text() == obj_strategy.get_user_id() and i_widget.tableWidget_Trade_Args.item(i_row, 3).text() == obj_strategy.get_strategy_id():
                        position = obj_strategy.get_position()['position_a_buy'] + obj_strategy.get_position()['position_a_sell']
                        i_widget.tableWidget_Trade_Args.item(i_row, 5).setText(str(position))  # 总持仓
                        i_widget.tableWidget_Trade_Args.item(i_row, 6).setText(str(obj_strategy.get_position()['position_a_buy']))  # 买持仓
                        i_widget.tableWidget_Trade_Args.item(i_row, 7).setText(str(obj_strategy.get_position()['position_a_sell']))  # 卖持仓
                        i_widget.tableWidget_Trade_Args.item(i_row, 8).setText('shouxufei')  # 持仓盈亏
                        i_widget.tableWidget_Trade_Args.item(i_row, 9).setText('shouxufei')  # 平仓盈亏
                        i_widget.tableWidget_Trade_Args.item(i_row, 10).setText('shouxufei')  # 手续费
                        i_widget.tableWidget_Trade_Args.item(i_row, 11).setText('chengjiaoliang')  # 成交量
                        i_widget.tableWidget_Trade_Args.item(i_row, 12).setText("chengjiaojin'e")  # 成交金额
                        i_widget.tableWidget_Trade_Args.item(i_row, 13).setText('pingjunhuadian')  # 平均滑点
                        # 缺少统计类指标。。。待续

    # 更新策略开关在Item中的显示文字“开”或者“关”，一个策略对应两个窗口（总账户窗口、策略所属的单账户窗口）
    def update_tableWidgetItem_Onoff(self, obj_strategy):
        # 遍历窗口
        for i_widget in self.__list_QAccountWidget:
            if i_widget.get_widget_name() in [obj_strategy.get_user_id(), "所有账户"]:
                for i_row in range(self.tableWidget_Trade_Args.rowCount()):  # 遍历界面的策略参数表
                    # 找到行的user_id、strategy_id与策略实例一致
                    if i_widget.tableWidget_Trade_Args.item(i_row, 2).text() == obj_strategy.get_user_id() \
                            and i_widget.tableWidget_Trade_Args.item(i_row, 3).text() == obj_strategy.get_strategy_id():
                        pass


# 创建user进程，形参为创建user初始化user所需要的所有信息，该函数被SocketManager中的信号调用
# def create_user_process(dict):
#     p = Process(target=global_create_user, args=(i,))  # self.__dict_total_user_process,))  # 创建user独立进程
#     # self.__dict_total_user_process[i['userid']].append(p)  # user独立进程
#     p.start()  # 开始进程

if __name__ == '__main__':
    multiprocessing.freeze_support()
    frozen = 'not'
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS

    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    win32api.SetDllDirectory(bundle_dir)
    sys.path.append(bundle_dir)

    # 删除log文件夹，创建log文件夹
    if os.path.exists('log'):
        pass  # 已存在文件夹，什么都不用操作
        # print("ClientMin.'__main__' log文件夹存在，删除重建log文件夹")
        # shutil.rmtree('log')
    else:
        # print("ClientMin.'__main__' log文件夹不存在，创建log文件夹")
        os.mkdir('log')

    # # 标准输出重新定向保存到本地log
    # time_str = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    # file_path_error = 'log/error_' + time_str + '.log'
    # stderr_handler = open(file_path_error, 'w')
    # sys.stderr = stderr_handler
    #
    # file_path_stdout = 'log/out_' + time_str + '.log'
    # stdout_handler = open(file_path_stdout, 'w')
    # sys.stdout = stdout_handler
    # print('we are', frozen, 'frozen')
    # print('bundle dir is', bundle_dir)
    # print('sys.argv[0] is', sys.argv[0])
    # print('sys.executable is', sys.executable)
    # print('os.getcwd is', os.getcwd())
    # print('process_id =', os.getpid(), 'thread.getName()=', threading.current_thread().getName(), ', __main__')

    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    file = QtCore.QFile('img/silvery.css')
    file.open(QtCore.QFile.ReadOnly)
    styleSheet = file.readAll().data().decode("utf-8")
    file.close()

    """创建对象"""
    # client_main = ClientMain()  # 创建客户端管理类对象
    # ctp_manager = CTPManager()  # 创建内核管理类对象
    xml_manager = XML_Manager()  # 创建XML管理对象
    socket_manager = SocketManager()  # 创建SocketManager对象   "192.168.180.130", 8888
    q_login = QLogin.QLoginForm()  # 登录窗口
    q_ctp = QCTP()  # 客户端主窗口
    q_alert_box = QAlertBox()  # 提示窗口
    q_login.show()

    q_login.set_SocketManager(socket_manager)
    socket_manager.set_XML_Manager(xml_manager)  # xml_manager设置为石头创可贴socket_manager的属性
    socket_manager.set_QLogin(q_login)
    socket_manager.set_QCTP(q_ctp)
    socket_manager.set_QAlert(q_alert_box)
    q_ctp.widget_QAccountWidget.set_SocketManager(socket_manager)
    q_ctp.widget_QOrderWidget.set_SocketManager(socket_manager)
    socket_manager.set_QAccountWidget(q_ctp.widget_QAccountWidget)
    socket_manager.set_QOrderWidget(q_ctp.widget_QOrderWidget)
    q_ctp.set_QLogin(q_login)

    # socket_manager.connect()  # 建立socket连接
    socket_manager.start()


    """设置属性"""
    # client_main.set_CTPManager(ctp_manager)
    # client_main.set_SocketManager(socket_manager)
    # client_main.set_QLoginForm(q_login)
    # client_main.set_QCTP(q_ctp)
    # ctp_manager.set_ClientMain(client_main)
    # ctp_manager.set_SocketManager(socket_manager)
    # ctp_manager.set_QLoginForm(q_login)
    # ctp_manager.set_QCTP(q_ctp)
    # ctp_manager.set_XML_Manager(xml_manager)
    # q_login.set_ClientMain(client_main)
    # q_login.set_CTPManager(ctp_manager)
    # q_login.set_SocketManager(socket_manager)
    # q_login.set_QCTP(q_ctp)
    # q_ctp.set_ClientMain(client_main)
    # q_ctp.set_CTPManager(ctp_manager)
    # q_ctp.set_SocketManager(socket_manager)
    # q_ctp.set_QLogin(q_login)
    # q_ctp.widget_QAccountWidget.set_ClientMain(client_main)
    # q_ctp.widget_QAccountWidget.set_CTPManager(ctp_manager)
    # q_ctp.widget_QAccountWidget.set_SocketManager(socket_manager)
    # q_ctp.widget_QAccountWidget.set_QLogin(q_login)

    """绑定信号槽"""
    # 定义信号：收到查询策略信息后出发信号 -> groupBox界面状态还原（激活查询按钮、恢复“设置持仓”按钮）
    socket_manager.signal_q_ctp_show.connect(q_ctp.show_me)
    # 定义信号，SocketManager发出信号 -> QAccountWidget创建tabBar
    socket_manager.signal_QAccountWidget_addTabBar.connect(q_ctp.widget_QAccountWidget.slot_addTabBar)
    # 绑定信号槽：SocketManager发出信号 -> QAccountWidget初始化tableWidget
    socket_manager.signal_init_tableWidget.connect(q_ctp.widget_QAccountWidget.slot_init_tableWidget)
    # 绑定信号槽：QLogin发送消息 -> SocketManager发送消息
    q_login.signal_send_msg.connect(socket_manager.slot_send_msg)
    # 绑定信号槽：SocketManager收到消息 -> 设置q_login消息框文本
    socket_manager.signal_label_login_error_text.connect(q_login.label_login_error.setText)
    # 绑定信号槽：SocketManager收到消息 -> 设置q_login的登录按钮是否可用
    socket_manager.signal_pushButton_login_set_enabled.connect(q_login.pushButton_login.setEnabled)
    # 绑定信号槽：SocketManager收到消息 -> 调用CTPManager的初始化方法
    # socket_manager.signal_ctp_manager_init.connect(ctp_manager.start_init)
    # 绑定信号槽：CTPManager -> 设置q_login消息框文本
    # ctp_manager.signal_label_login_error_text.connect(q_login.label_login_error.setText)
    # SocketManager收到服务端修改策略参数类回报 -> CTPManager修改策略（SocketManager.signal_update_strategy -> CTPManager.slot_update_strategy()）
    # socket_manager.signal_update_strategy.connect(ctp_manager.slot_update_strategy)
    # CTPManager初始化内核（子线程）向界面弹窗 -> ClientMain（主线程）调用槽函数向界面弹窗
    # ctp_manager.signal_show_QMessageBox.connect(client_main.slot_show_QMessageBox)
    # 绑定信号槽：定时刷新UI信号->定时刷新UI槽
    q_ctp.widget_QAccountWidget.signal_update_ui.connect(q_ctp.widget_QAccountWidget.slot_update_ui)
    # 绑定信号槽：界面发送策略按钮被点击->socket发送消息
    q_ctp.widget_QAccountWidget.signal_send_msg.connect(socket_manager.slot_send_msg)
    # 绑定信号槽：SocketManager获得list_instrument_id -> QAccountWidget创建新建策略窗口
    socket_manager.signal_create_QNewStrategy.connect(q_ctp.widget_QAccountWidget.create_QNewStrategy)
    # 绑定信号槽：SocketManager收到新建策略消息 -> 界面添加一行QAccountWidget.slot_insert_strategy
    # socket_manager.signal_insert_strategy.connect(q_ctp.widget_QAccountWidget.slot_insert_strategy)
    # 绑定信号槽: SocketManager发送data_list -> QAccountWidget.tableView_Trade_Args接收数据,刷新界面
    # socket_manager.signal_set_data_list.connect(q_ctp.widget_QAccountWidget.slot_set_data_list)
    # 绑定信号槽：SocketManger收到进程通信user进程发来的资金账户信息 -> 向界面发送数据，并更新界面
    socket_manager.signal_update_panel_show_account.connect(q_ctp.widget_QAccountWidget.slot_update_panel_show_account)
    # 绑定信号槽：SocketManager发送data_list -> QAccountWidget.tableView_Trade_Args接收数据,刷新界面
    # socket_manager.signal_set_data_list.connect(q_ctp.widget_QAccountWidget.StrategyDataModel.slot_set_data_list)
    # 绑定信号槽：右击菜单隐藏 -> 右击菜单信息初始化为空
    q_ctp.widget_QAccountWidget.popMenu.aboutToHide.connect(q_ctp.widget_QAccountWidget.slot_init_right_click)
    # 绑定信号槽：SocketManager收到查询策略回报消息 -> 向界面发送信号，激活查询策略按钮
    socket_manager.signal_activate_query_strategy_pushbutton.connect(q_ctp.widget_QAccountWidget.slot_activate_query_strategy_pushbutton)

    # 绑定信号槽：SocketManager收到修改策略回报 -> 界面tableView更新特定index
    socket_manager.signal_update_strategy_on_off.connect(q_ctp.widget_QAccountWidget.StrategyDataModel.slot_update_strategy_on_off)
    # 绑定信号槽：SocketManager收到下单算法信息 -> 界面groupBox初始化下单算法选项
    socket_manager.signal_init_groupBox_order_algorithm.connect(q_ctp.widget_QAccountWidget.slot_init_groupBox_order_algorithm)
    # 绑定信号槽：SocketManager收到交易员登录成功信息 -> 初始化界面“开始策略”按钮
    socket_manager.signal_init_ui_on_off.connect(q_ctp.widget_QAccountWidget.slot_init_ui_on_off)
    # 绑定信号槽：触发弹窗 -> 显示弹窗
    # socket_manager.signal_show_message.connect(socket_manager.msg_box.showMessage_list)
    socket_manager.signal_setTabIcon.connect(q_ctp.widget_QAccountWidget.slot_setTabIcon)  # 绑定信号槽：Socket收到修改期货账户开关或交易员开关 -> 设置tabbar样式
    socket_manager.signal_init_setTabIcon.connect(q_ctp.widget_QAccountWidget.slot_init_setTabIcon)  # 绑定信号槽：初始化tab样式
    q_ctp.widget_QAccountWidget.signal_show_alert.connect(q_alert_box.slot_show_alert)  # 绑定信号槽：显示弹窗
    socket_manager.signal_show_alert.connect(q_alert_box.slot_show_alert)  # 绑定信号槽：显示弹窗
    socket_manager.signal_on_pushButton_set_position_active.connect(q_ctp.widget_QAccountWidget.on_pushButton_set_position_active)  # 绑定信号槽：socket收到设置持仓消息 -> 激活界面设置持仓按钮

    # 设置字体大小
    # font = app.font()
    # font.setPointSize(10)
    # app.setFont(font)
    sys.exit(app.exec_())


