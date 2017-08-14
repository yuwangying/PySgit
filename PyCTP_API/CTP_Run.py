# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 00:31:14 2016

@author: Zhuolin
"""

import sys
import time
import os
import threading
import chardet
import pandas as pd
from pandas import Series, DataFrame
import FunctionLog
from Trade import PyCTP_Trader
from Market import PyCTP_Market
import Utils


def __main__():
    BrokerID = b'9999'
    UserID = b'063802'  # 063802
    Password = b'123456'  # 123456
    ExchangeID = b'SHFE'
    listInstrumentID = [b'cu1701', b'cu1612']
    InstrumentID = b'cu1701'
    trader = PyCTP_Trader.CreateFtdcTraderApi(b'tmp/_tmp_t_')  # Trade实例
    market = PyCTP_Market.CreateFtdcMdApi(b'tmp/_tmp_m_')  # Market实例
    print('连接交易前置', Utils.code_transform(trader.Connect(b'tcp://180.168.146.187:10000')))
    print('连接行情前置', Utils.code_transform(market.Connect(b'tcp://180.168.146.187:10010')))
    print('交易账号登陆', Utils.code_transform(trader.Login(BrokerID, UserID, Password)))
    print('交易账号登陆', Utils.code_transform(market.Login(BrokerID, UserID, Password)))
    print('交易日', Utils.code_transform(trader.GetTradingDay()))
    print('设置投资者代码', Utils.code_transform(trader.setInvestorID(UserID)))
    # time.sleep(1.0)
    # print('查询交易所', Utils.code_transform(trader.QryExchange()))
    # time.sleep(1.0)
    # print('查询投资者', Utils.code_transform(trader.QryInvestor()))
    # time.sleep(1.0)
    # print('查询资金账户', Utils.code_transform(trader.QryTradingAccount()))
    # time.sleep(1.0)
    # print('查询合约', Utils.code_transform(trader.QryInstrument(b'SHFE')))
    # time.sleep(1.0)
    # dfInstrument.to_csv('data/dfInstrument.csv')
    # time.sleep(1.0)
    # print('查询交易代码', Utils.code_transform(trader.QryTradingCode(ExchangeID)))
    # time.sleep(1.0)
    # print('合约手续费率', Utils.code_transform(trader.QryInstrumentCommissionRate(InstrumentID)))
    # time.sleep(1.0)
    # print('合约保证金率', Utils.code_transform(trader.QryInstrumentMarginRate(InstrumentID)))
    # time.sleep(1.0)
    # print('查询报单', Utils.code_transform(trader.QryOrder()))
    # time.sleep(1.0)
    # print('查询成交单', Utils.code_transform(trader.QryTrade()))
    # time.sleep(1.0)
    # print('投资者持仓', Utils.code_transform(trader.QryInvestorPosition()))
    # time.sleep(1.0)
    # print('查询行情', Utils.code_transform(trader.QryDepthMarketData(InstrumentID)))
    # time.sleep(1.0)
    # print('订阅行情', Utils.code_transform(market.SubMarketData(listInstrumentID)))

    # 调试OrderInsert
    while True:
        Utils.print_menu()
        var = input()

        if var == '1':
            print('查询交易所\n', Utils.code_transform(trader.QryExchange()))
            continue

        if var == '2':
            print('请选择要查询的交易所合约信息：\ns = 上海期货交易所\nd = 大连商品交易所\nz = 郑州商品交易所\nc = 中国金融期货交易所\na = 以上所有交易所')
            var = input()
            if var == 's':
                input_params = b'SHFE'
            elif var == 'd':
                input_params = b'DCE'
            elif var == 'z':
                input_params = b'CZCE'
            elif var == 'c':
                input_params = b'CFFEX'
            elif var == 'a':
                input_params = b''
            else:
                print('输入错误')
                continue
            print('查询合约', Utils.code_transform(trader.QryInstrument(input_params)))
            continue

        if var == '3':
            print('查询合约状态\n', Utils.code_transform(trader.QryInvestor()))
            continue

        if var == '4':
            print('查询账户信息\n', Utils.code_transform(trader.QryInvestor()))
            continue

        if var == '5':
            print('查询账户资金\n', Utils.code_transform(trader.QryTradingAccount()))
            continue

        if var == '6':
            print('查询账户持仓汇总\n', Utils.code_transform(trader.QryInvestorPosition()))
            continue

        if var == '7':
            print('查询账户持仓明细\n', Utils.code_transform(trader.QryInvestorPositionDetail()))
            continue

        if var == '8':
            print('查询委托记录\n', Utils.code_transform(trader.QryOrder()))
            continue

        if var == '9':
            print('查询交易记录\n', Utils.code_transform(trader.QryTrade()))
            continue

        if var == '10':
            print('please input OrderInsert arguments dict:\n')
            input_params = input()
            try:
                input_params = eval(input_params)
            except SyntaxError as e:
                print('except:', e)
                print('输入参数错误')
                continue
            print('输入参数为\n', input_params)
            trader.OrderInsert(InstrumentID=input_params['InstrumentID'],
                               Action=input_params['Action'],
                               Direction=input_params['Direction'],
                               Volume=input_params['Volume'],
                               Price=input_params['Price'],
                               OrderRef=input_params['OrderRef'])
            continue

        # 进入OrderAction命令模式
        if var == '10':
            print('please input OrderAction arguments:\n')
            input_params = input()
            try:
                input_params = eval(input_params)
            except SyntaxError as e:
                print('except:', e)
                print('输入参数错误')
                continue
            print('输入参数为\n', input_params)
            trader.OrderAction(ExchangeID=input_params['ExchangeID'],
                               OrderRef=input_params['OrderRef'],
                               OrderSysID=input_params['OrderSysID'])
            continue

        # 保存文件到本地
        if var == 's':
            path_tmp = 'data/'+trader.get_UserID().decode()+'_QryInstrument.csv'
            PyCTP_Trader.dfQryInstrument.to_csv(path_tmp)
            path_tmp = 'data/' + trader.get_UserID().decode() + '_QryInstrumentStatus.csv'
            PyCTP_Trader.dfQryInstrumentStatus.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_QryInvestorPosition.csv'
            PyCTP_Trader.dfQryInvestorPosition.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_QryInvestorPositionDetail.csv'
            PyCTP_Trader.dfQryInvestorPositionDetail.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_OnRtnOrder.csv'
            PyCTP_Trader.dfOnRtnOrder.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_OnRtnTrade.csv'
            PyCTP_Trader.dfOnRtnTrade.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_QryOrder.csv'
            PyCTP_Trader.dfQryOrder.to_csv(path_tmp)
            path_tmp = 'data/'+trader.get_UserID().decode()+'_QryTrade.csv'
            PyCTP_Trader.dfQryTrade.to_csv(path_tmp)
            continue

        # 退出
        if var == 'q':
            break

        # 输入错误重新输入
        if True:
            print('input error, please input again\n')
            continue
            # 保存数据到本地

    time.sleep(1.0)
    print('退订行情:', market.UnSubMarketData(listInstrumentID))
    print('交易账号登出', trader.Logout())
    print('行情账号登出', market.Logout())


if __name__ == '__main__':
    __main__()

