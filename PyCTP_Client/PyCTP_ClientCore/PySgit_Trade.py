from datetime import datetime
import pyctp
# import sys
# from time import time
# import threading
# import pandas as pd
# from pandas import Series, DataFrame
# import Utils
# import copy


class PySgit_Trade_API(pyctp.CSgitFtdcTraderSpi):
    request_id = 0

    def __init__(self, frontaddress, broker_id, user_id, password):
        pyctp.CSgitFtdcTraderSpi.__init__(self)

        self.frontaddress = frontaddress
        self.broker_id = broker_id
        self.user_id = user_id
        self.password = password

        self.api = pyctp.CSgitFtdcTraderApi_CreateFtdcTraderApi("./conn/sgit_td/")
        self.api.SubscribePrivateTopic(pyctp.Sgit_TERT_RESTART)
        self.api.SubscribePublicTopic(pyctp.Sgit_TERT_RESTART)
        self.api.RegisterSpi(self)
        self.api.RegisterFront(self.frontaddress)
        self.api.Init(True)  # 对应spi方法OnFrontConnected

    def set_user(self, obj_user):
        self.__user = obj_user

    def join(self):
        self.api.Join()

    def Login(self):
        field = pyctp.CSgitFtdcReqUserLoginField()
        field.BrokerID = self.broker_id
        field.UserID = self.user_id
        field.Password = self.password
        request_id = 1
        print(">>>PySgit_Trade_API.Login() called")
        self.api.ReqUserLogin(field, request_id)

    def OnFrontConnected(self):
        print(">>>PySgit_Trade_API.OnFrontConnected() called")
        self.Login()

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        print(">>>PySgit_Trade_API.OnRspUserLogin() called")
        self.api.Ready()

    def OnRtnOrder(self, OrderField, pRspInfo):
        # print(">>>PySgit_Trade_API.OnRtnOrder() called")
        if pRspInfo.ErrorID == 0:  # 报单成功
            pass
        else:  # 报单失败
            print(">>>PySgit_Trade_API.OnRtnOrder() ErrorID =", pRspInfo.ErrorID)
            # return

        Order = {
            'BrokerID': OrderField.BrokerID,  # 经纪公司代码
            'InvestorID': OrderField.InvestorID,  # 投资者代码
            'InstrumentID': OrderField.InstrumentID,  # 合约代码
            'OrderRef': OrderField.OrderRef,  # 报单引用
            'UserID': OrderField.UserID,  # 用户代码
            'OrderPriceType': OrderField.OrderPriceType,  # 报单价格条件
            'Direction': OrderField.Direction,  # 买卖方向
            'CombOffsetFlag': OrderField.CombOffsetFlag,  # 组合开平标志
            'CombHedgeFlag': OrderField.CombHedgeFlag,  # 组合投机套保标志
            'LimitPrice': OrderField.LimitPrice,  # 价格
            'VolumeTotalOriginal': OrderField.VolumeTotalOriginal,  # 数量
            # 'TimeCondition': OrderField.TimeCondition,  # 有效期类型
            # 'GTDDate': OrderField.GTDDate,  # GTD日期
            'VolumeCondition': OrderField.VolumeCondition,  # 成交量类型
            'MinVolume': OrderField.MinVolume,  # 最小成交量
            # 'ContingentCondition': OrderField.ContingentCondition,  # 触发条件
            # 'StopPrice': OrderField.StopPrice,  # 止损价
            'ForceCloseReason': OrderField.ForceCloseReason,  # 强平原因
            # 'IsAutoSuspend': OrderField.IsAutoSuspend,  # 自动挂起标志
            # 'BusinessUnit': OrderField.BusinessUnit,  # 业务单元
            'RequestID': OrderField.RequestID,  # 请求编号
            'OrderLocalID': OrderField.OrderLocalID,  # 本地报单编号
            'ExchangeID': OrderField.ExchangeID,  # 交易所代码
            'ParticipantID': OrderField.ParticipantID,  # 会员代码
            'ClientID': OrderField.ClientID,  # 客户代码
            'ExchangeInstID': OrderField.ExchangeInstID,  # 合约在交易所的代码
            'TraderID': OrderField.TraderID,  # 交易所交易员代码
            # 'InstallID': OrderField.InstallID,  # 安装编号
            'OrderSubmitStatus': OrderField.OrderSubmitStatus,  # 报单提交状态
            # 'NotifySequence': OrderField.NotifySequence,  # 报单提示序号
            'TradingDay': OrderField.TradingDay,  # 交易日
            # 'SettlementID': OrderField.SettlementID,  # 结算编号
            'OrderSysID': OrderField.OrderSysID,  # 报单编号
            # 'OrderSource': OrderField.OrderSource,  # 报单来源
            # 'OrderStatus': OrderField.OrderStatus,  # 报单状态
            'OrderType': OrderField.OrderType,  # 报单类型
            'VolumeTraded': OrderField.VolumeTraded,  # 今成交数量
            'VolumeTotal': OrderField.VolumeTotal,  # 剩余数量
            'InsertDate': OrderField.InsertDate,  # 报单日期，mini2柜台返回的该字段为空
            # 'InsertDate': date,  # 报单日期
            'InsertTime': OrderField.InsertTime,  # 委托时间
            'ActiveTime': OrderField.ActiveTime,  # 激活时间
            'SuspendTime': OrderField.SuspendTime,  # 挂起时间
            'UpdateTime': OrderField.UpdateTime,  # 最后修改时间
            'CancelTime': OrderField.UpdateTime,  # 撤销时间
            # 'ActiveTraderID': OrderField.ActiveTraderID,  # 最后修改交易所交易员代码
            # 'ClearingPartID': OrderField.ClearingPartID,  # 结算会员编号
            # 'SequenceNo': OrderField.SequenceNo,  # 序号
            'FrontID': OrderField.FrontID,  # 前置编号
            'SessionID': OrderField.SessionID,  # 会话编号
            # 'UserProductInfo': OrderField.UserProductInfo,  # 用户端产品信息
            # 'StatusMsg': OrderField.StatusMsg,  # 状态信息
            # 'UserForceClose': OrderField.UserForceClose,  # 用户强评标志
            # 'ActiveUserID': OrderField.ActiveUserID,  # 操作用户代码
            # 'BrokerOrderSeq': OrderField.BrokerOrderSeq,  # 经纪公司报单编号
            # 'RelativeOrderSysID': OrderField.RelativeOrderSysID,  # 相关报单
            # 'ZCETotalTradedVolume': OrderField.ZCETotalTradedVolume,  # 郑商所成交数量
            # 'IsSwapOrder': OrderField.IsSwapOrder,  # 互换单标志
            # 'BranchID': OrderField.BranchID,  # 营业部编号
            # 'InvestUnitID': OrderField.InvestUnitID,  # 投资单元代码
            # 'AccountID': OrderField.AccountID,  # 资金账号
            # 'CurrencyID': OrderField.CurrencyID,  # 币种代码
            # 'IPAddress': OrderField.IPAddress,  # IP地址
            # 'MacAddress': OrderField.MacAddress  # Mac地址
        }
        # print(">>>PySgit_Trade_API.OnRtnOrder() Order =", Order)
        # print(">>>PySgit_Trade_API.OnRtnOrder() Order['OrderRef'] =", Order['OrderRef'])
        # print(">>>时序测试 OrderRef =", Order['OrderRef'], "OnRtnOrder()")
        self.__user.OnRtnOrder(Order)  # 转回调给User类的OnRtnOrder

    def OnRtnTrade(self, TradeField):
        # print(">>>PySgit_Trade_API.OnRtnTrade() called")
        date = datetime.now().strftime('%Y%m%d')
        Trade = {
            'BrokerID': TradeField.BrokerID,  # 经纪公司代码
            'InvestorID': TradeField.InvestorID,  # 投资者代码
            'InstrumentID': TradeField.InstrumentID,  # 合约代码
            'OrderRef': TradeField.OrderLocalID,  # 报单引用，飞鼠中的OrderLocalID等于CTP中的OrderRef
            'UserID': TradeField.UserID,  # 用户代码
            'ExchangeID': TradeField.ExchangeID,  # 交易所代码
            'TradeID': TradeField.TradeID,  # 成交编号
            'Direction': TradeField.Direction,  # 买卖方向
            'OrderSysID': TradeField.OrderSysID,  # 报单编号
            'ParticipantID': TradeField.ParticipantID,  # 会员代码
            'ClientID': TradeField.ClientID,  # 客户代码
            'TradingRole': TradeField.TradingRole,  # 交易角色
            'ExchangeInstID': TradeField.ExchangeInstID,  # 合约在交易所的代码
            'OffsetFlag': TradeField.OffsetFlag,  # 开平标志
            'HedgeFlag': TradeField.HedgeFlag,  # 投机套保标志
            'Price': TradeField.Price,  # 价格
            'Volume': TradeField.Volume,  # 数量
            # 'TradeDate': TradeField.TradeDate,  # 成交时期
            'TradeDate': date,  # 成交时期
            'TradeTime': TradeField.TradeTime,  # 成交时间
            # 'TradeTime': time,  # 成交时间
            'TradeType': TradeField.TradeType,  # 成交类型
            'PriceSource': TradeField.PriceSource,  # 成交价来源
            'TraderID': TradeField.TraderID,  # 交易所交易员代码
            'OrderLocalID': TradeField.OrderLocalID,  # 本地报单编号
            'ClearingPartID': TradeField.ClearingPartID,  # 结算会员编号
            'BusinessUnit': TradeField.BusinessUnit,  # 业务单元
            'SequenceNo': TradeField.SequenceNo,  # 序号
            'TradingDay': TradeField.TradingDay,  # 交易日
            'SettlementID': TradeField.SettlementID,  # 结算编号
            'BrokerOrderSeq': TradeField.BrokerOrderSeq,  # 经纪公司报单编号
            'TradeSource': TradeField.TradeSource  # 成交来源
        }
        # print(">>>PySgit_Trade_API.OnRtnTrade() Trade =", Trade)
        self.__user.OnRtnTrade(Trade)  # 转到user回调函数

    # 撤单回报
    def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        # print(">>>PySgit_Trade_API.OnRspOrderAction() called")
        # 撤单成功
        if pRspInfo.ErrorID == 0:
            if pInputOrderAction is not None:
                OrderAction = {
                    'BrokerID': pInputOrderAction.BrokerID,
                    'InvestorID': pInputOrderAction.InvestorID,
                    'OrderActionRef': pInputOrderAction.OrderActionRef,
                    'OrderRef': pInputOrderAction.OrderRef,
                    'RequestID': pInputOrderAction.RequestID,
                    'FrontID': pInputOrderAction.FrontID,
                    'SessionID': pInputOrderAction.SessionID,
                    'ExchangeID': pInputOrderAction.ExchangeID,
                    'OrderSysID': pInputOrderAction.OrderSysID,
                    'ActionFlag': pInputOrderAction.ActionFlag,
                    'LimitPrice': pInputOrderAction.LimitPrice,
                    'VolumeChange': pInputOrderAction.VolumeChange,
                    'UserID': pInputOrderAction.UserID,
                    'InstrumentID': pInputOrderAction.InstrumentID
                }
                # print(">>>PySgit_Trade_API.OnRspOrderAction() OrderAction =", OrderAction)
                # print(">>>时序测试 OrderRef =", OrderAction['OrderRef'], "OnRspOrderAction()")
                self.__user.OnRspOrderAction(OrderAction)  # 转到user回调函数
            else:
                # print(">>>PySgit_Trade_API.OnRspOrderAction() pInputOrderAction is None")
                pass
        # 撤单失败，不需要处理
        else:
            print_str = pRspInfo.ErrorID
            # print_str = pRspInfo.ErrorMsg  # pRspInfo中没有ErrorMsg，该代码导致user进程异常退出
            # print(">>>PySgit_Trade_API.OnRspOrderAction() 撤单失败，ErrorID =", print_str)
