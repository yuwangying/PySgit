import pandas as pd
from pandas import DataFrame, Series


class TradeModel():
    def __init__(self):
        pass

    # 交易模型共用属性:市场行情等
    def init_market_data(self, dict_args):
        self.__df_market = DataFrame()  # 时序数据
        self.__a_instrument_id = dict_args['a_instrument_id']
        self.__a_commission_rate = dict_args['a_commission_rate']  # dict,A手续费率
        self.__a_multiple = dict_args['a_commission_rate']  # int,A合约乘数
        self.__b_instrument_id = dict_args['b_instrument_id']
        self.__b_commission_rate = dict_args['b_commission_rate']  # dict,A手续费率
        self.__b_multiple = dict_args['b_commission_rate']  # int,B合约乘数

    # 选择交易模型
    def select_trade_model(self, int_input):
        self.__select_model = int_input

    # 交易模型1
    def trade_model_one(self):
        pass

    # 初始化交易模型
    def init_trade_model_one(self):
        pass

    # 交易模型2
    def trade_model_two(self):
        pass