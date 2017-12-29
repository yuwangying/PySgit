import urllib.parse
from pymongo import MongoClient
import datetime
import pandas as pd
# import queue
# from sys import getsizeof


class MarketDataModel():
    # 创建一个具有maximum_connections的mongodb带权限验证的连接池
    # ipaddr => mongodb server ip
    # port => mongod server port
    # dbname => mongodb database name
    # name => mongodb name of user
    # pwd => mongodb password of user
    # collection_name => the collection_name you want to operate
    def __init__(self, ipaddr, port, dbname, name, pwd):
        # 创建连接
        username = urllib.parse.quote_plus(name)
        password = urllib.parse.quote_plus(pwd)
        uri = "mongodb://" + username + ":" + password + "@" + ipaddr + ":" + str(port) + "/admin?authMechanism=SCRAM-SHA-1"
        self.client = MongoClient(uri)  # 连接实例
        # print("self.client.database_names() =", self.client.database_names())  # list，数据库名称
        self.db = self.client[dbname]  # 数据库链接
        # print("self.db.collection_names() =", self.db.collection_names())  # list，某一个数据里面的集合名称
        # print("20171031" in self.db.collection_names())  # bool,集合名称是否存在于数据库中
        # self.col_op = self.db[collection_name]  # 集合链接
        # self.col_op.create_index("InstrumentID", background=True)  # 创建索引
        # self.col_op.drop_indexes()
        print(">>>MarketDataModel.__init__() finished")

    # 生成group_tick，形参：合约代码A,合约代码B,将加入到集合中的tick,集合tick
    def transform_tick_group(self, instrument_id_a, instrument_id_b, tick, tick_group):
        # 标明tick_group中存在的合约行情
        if tick_group is None:
            tick_group = dict()
            if tick['InstrumentID'] == instrument_id_a:
                tick_group['InstrumentExist'] = 'Ab'
                # B的行情先填空值
                tick_group['InstrumentID_b'] = ''
                tick_group['LastPrice_b'] = ''
                tick_group['AskPrice1_b'] = ''
                tick_group['AskVolume1_b'] = ''
                tick_group['BidPrice1_b'] = ''
                tick_group['BidVolume1_b'] = ''
                tick_group['UpperLimitPrice_b'] = ''
                tick_group['LowerLimitPrice_b'] = ''
                tick_group['OpenInterest_b'] = ''
                tick_group['Volume_b'] = ''
            if tick['InstrumentID'] == instrument_id_b:
                tick_group['InstrumentExist'] = 'aB'
                # A的行情先填空值
                tick_group['InstrumentID_a'] = ''
                tick_group['LastPrice_a'] = ''
                tick_group['AskPrice1_a'] = ''
                tick_group['AskVolume1_a'] = ''
                tick_group['BidPrice1_a'] = ''
                tick_group['BidVolume1_a'] = ''
                tick_group['UpperLimitPrice_a'] = ''
                tick_group['LowerLimitPrice_a'] = ''
                tick_group['OpenInterest_a'] = ''
                tick_group['Volume_a'] = ''
        else:
            if tick_group['InstrumentExist'] == 'Ab':  # A已存在tick_group，加入B数据
                if tick['InstrumentID'] == instrument_id_b:
                    tick_group['InstrumentExist'] = 'AB'
            if tick_group['InstrumentExist'] == 'aB':  # B已存在tick_group，加入A数据
                if tick['InstrumentID'] == instrument_id_a:
                    tick_group['InstrumentExist'] = 'AB'
        if tick['InstrumentID'] == instrument_id_a:
            tick_group['InstrumentID_a'] = tick['InstrumentID']
            tick_group['LastPrice_a'] = tick['LastPrice']
            tick_group['AskPrice1_a'] = tick['AskPrice1']
            tick_group['AskVolume1_a'] = tick['AskVolume1']
            tick_group['BidPrice1_a'] = tick['AskPrice1']
            tick_group['BidVolume1_a'] = tick['BidVolume1']
            tick_group['UpperLimitPrice_a'] = tick['UpperLimitPrice']
            tick_group['LowerLimitPrice_a'] = tick['LowerLimitPrice']
            tick_group['OpenInterest_a'] = tick['OpenInterest']
            tick_group['Volume_a'] = tick['Volume']
            tick_group['UpdateMillisec'] = tick['UpdateMillisec']
            tick_group['UpdateTime'] = tick['UpdateTime']
            tick_group['TradingDay'] = tick['TradingDay']
        elif tick['InstrumentID'] == instrument_id_b:
            tick_group['InstrumentID_b'] = tick['InstrumentID']
            tick_group['LastPrice_b'] = tick['LastPrice']
            tick_group['AskPrice1_b'] = tick['AskPrice1']
            tick_group['AskVolume1_b'] = tick['AskVolume1']
            tick_group['BidPrice1_b'] = tick['AskPrice1']
            tick_group['BidVolume1_b'] = tick['BidVolume1']
            tick_group['UpperLimitPrice_b'] = tick['UpperLimitPrice']
            tick_group['LowerLimitPrice_b'] = tick['LowerLimitPrice']
            tick_group['OpenInterest_b'] = tick['OpenInterest']
            tick_group['Volume_b'] = tick['Volume']
            tick_group['UpdateMillisec'] = tick['UpdateMillisec']
            tick_group['UpdateTime'] = tick['UpdateTime']
            tick_group['TradingDay'] = tick['TradingDay']
        return tick_group  # 待续2017年10月19日15:12:06：输出的tick_group中A、B合约一定都存在值
    
    # 返回list中最后一个指定合约代码的LastPrice
    # 返回list_input中键名为key_InstrumentID最后一个存在键值key_LastPrice
    def last_price(self, list_input, instrument_id, key_InstrumentID, key_LastPrice):
        len_list_input = len(list_input)
        for i in range(len_list_input):
            last = len_list_input - i - 1  # last：逆序遍历list_input的游标
            if list_input[last][key_InstrumentID] == instrument_id:
                return list_input[last][key_LastPrice]
        return None
    
    # 给定交易日，返回前一个交易日的日期，7个交易日内不存在行情则返回None
    def pre_tradingday_date(self, str_date):
        datetime_tradingday = datetime.datetime.strptime(str_date, "%Y%m%d")
        for i in range(1, 8, 1):
            datetime_tradingday_pre = datetime_tradingday - datetime.timedelta(days=i)
            str_tradingday_pre = datetime_tradingday_pre.strftime("%Y%m%d")
            if str_tradingday_pre in market_data_model.db.collection_names():
                return str_tradingday_pre
        return None

    # 将两个合约的行情组合成一个list
    def compound_tick(self, instrument_id_a, instrument_id_b, str_date):
        list_tick_group = list()  # 返回值
        # projection_filter = {"_id": 0,
        #                      "InstrumentID": 1,
        #                      "LastPrice": 1,
        #                      "Volume": 1,
        #                      "AskPrice1": 1,
        #                      "BidPrice1": 1,
        #                      "AskVolume1": 1,
        #                      "BidVolume1": 1,
        #                      "UpdateTime": 1,
        #                      "UpdateMillisec": 1,
        #                      "OpenPrice": 1,
        #                      "HighestPrice": 1,
        #                      "TradingDay": 1,
        #                      "UpperLimitPrice": 1,
        #                      "LowerLimitPrice": 1
        #                      }
        # self.col_op = self.db[collection_name]  # 集合链接
        data_cursor = self.db[str_date].find(
            filter={'InstrumentID': {"$in": [instrument_id_a, instrument_id_b]}},
            # projection=projection_filter,
            projection={'_id': 0},
            no_cursor_timeout=True)
        for tick in data_cursor:
            # 过滤掉非交易时间内的行情
            if (tick['UpdateTime'] > '15:00:00' and tick['UpdateTime'] < '21:00:00') or (
                    tick['UpdateTime'] > '02:30:00' and tick['UpdateTime'] < '09:00:00'):
                continue  # 跳出本次循环
            len_list_tick_group = len(list_tick_group)
            last = len_list_tick_group - 1  # list_tick_group最后一个元素的index
            if len_list_tick_group > 0:
                # 最新tick合约代码存在于最后一条tick_group中，则将最新tick存入到新加入行
                if tick['InstrumentID'] in list_tick_group[last]:
                    tick_group = market_data_model.transform_tick_group(instrument_id_a, instrument_id_b, tick, None)
                    list_tick_group.append(tick_group)
                elif tick['InstrumentID'] not in list_tick_group[last]:
                    # 最新tick的行情时间等于最后一条tick_group中已经存在的另外一个合约的行情时间，则合并在tick_group最后一行
                    if tick['UpdateTime'] == list_tick_group[last]['UpdateTime'] \
                            and tick['UpdateMillisec'] == list_tick_group[last]['UpdateMillisec']:
                        tick_group = market_data_model.transform_tick_group(instrument_id_a, instrument_id_b, tick,
                                                                            list_tick_group[last])
                        list_tick_group[last] = tick_group
                    # 最新tick的行情时间小于最后一条tick_group中已经存在的行情时间
                    elif tick['UpdateTime'] < list_tick_group[last]['UpdateTime'] \
                            or (tick['UpdateTime'] == list_tick_group[last]['UpdateTime']
                                and tick['UpdateMillisec'] < list_tick_group[last]['UpdateMillisec']):
                        # 特殊情况：换了自然日，最新tick更新时间是00:00:00之后，最后一条tick_group更新时间是23:59:59之前，则新的tick添加到新一行tick_group
                        if '21:00:00' <= list_tick_group[last]['UpdateTime'] and list_tick_group[last][
                            'UpdateTime'] <= '23:59:59' \
                                and '00:00:00' <= tick['UpdateTime'] and tick['UpdateTime'] <= '15:00:00':
                            tick_group = market_data_model.transform_tick_group(instrument_id_a, instrument_id_b, tick,
                                                                                None)
                            list_tick_group.append(tick_group)
                        # 其他情况：错误时序数据，不处理
                        else:
                            pass
                    # 最新tick的行情时间大于最后一条tick_group中已经存在的行情时间，则新的tick添加到新一行tick_group
                    elif tick['UpdateTime'] > list_tick_group[last]['UpdateTime'] \
                            or (tick['UpdateTime'] == list_tick_group[last]['UpdateTime']
                                and tick['UpdateMillisec'] > list_tick_group[last]['UpdateMillisec']):
                        tick_group = market_data_model.transform_tick_group(instrument_id_a, instrument_id_b, tick,
                                                                            None)
                        list_tick_group.append(tick_group)
            elif len_list_tick_group == 0:  # 集合tick里面还不存在数据
                tick_group = market_data_model.transform_tick_group(instrument_id_a, instrument_id_b, tick, None)
                list_tick_group.append(tick_group)  # 集合tick添加到list

            # 计算价差
            if list_tick_group[last]['InstrumentExist'] == 'AB':
                list_tick_group[last]['SpreadPrice'] = list_tick_group[last]['LastPrice_a'] - list_tick_group[last][
                    'LastPrice_b']
            elif list_tick_group[last]['InstrumentExist'] == 'aB':
                LastPrice_a = market_data_model.last_price(list_tick_group, instrument_id_a, 'InstrumentID_a',
                                                           'LastPrice_a')
                if LastPrice_a is not None:
                    list_tick_group[last]['SpreadPrice'] = LastPrice_a - list_tick_group[last]['LastPrice_b']
                elif LastPrice_a is None:
                    list_tick_group[last]['SpreadPrice'] = None
            elif list_tick_group[last]['InstrumentExist'] == 'Ab':
                LastPrice_b = market_data_model.last_price(list_tick_group, instrument_id_b, 'InstrumentID_b',
                                                           'LastPrice_b')
                if LastPrice_b is not None:
                    list_tick_group[last]['SpreadPrice'] = list_tick_group[last]['LastPrice_a'] - LastPrice_b
                elif LastPrice_b is None:
                    list_tick_group[last]['SpreadPrice'] = None

            # # 计算价差的指标
            # # if list_tick_group[last]['InstrumentExist'] == 'AB':
            # if len_list_tick_group > len_average:
            #     list_tick_group[last]['sum_SpreadPrice'] = list_tick_group[last - 1]['sum_SpreadPrice'] + \
            #                                                list_tick_group[last]['SpreadPrice'] - \
            #                                                list_tick_group[len_list_tick_group - len_average][
            #                                                    'SpreadPrice']
            #     list_tick_group[last]['ave_SpreadPrice'] = list_tick_group[last]['sum_SpreadPrice'] / len_average
            #     list_tick_group[last]['above_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] + band * min_move
            #     list_tick_group[last]['below_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] - band * min_move
            # elif 1 < len_list_tick_group <= len_average:
            #     try:
            #         list_tick_group[last]['sum_SpreadPrice'] = list_tick_group[last - 1]['sum_SpreadPrice'] + \
            #                                                    list_tick_group[last]['SpreadPrice']
            #     except:
            #         print("len_list_tick_group =", len_list_tick_group)
            #         print("last =", last)
            #         print("list_tick_group[last-1] =", list_tick_group[last - 1])
            #         print("list_tick_group[last-2] =", list_tick_group[last - 2])
            #         print("list_tick_group[last] =", list_tick_group[last])
            #     list_tick_group[last]['ave_SpreadPrice'] = list_tick_group[last][
            #                                                    'sum_SpreadPrice'] / len_list_tick_group
            #     list_tick_group[last]['above_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] + band * min_move
            #     list_tick_group[last]['below_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] - band * min_move
            # elif len_list_tick_group == 1:
            #     list_tick_group[last]['sum_SpreadPrice'] = list_tick_group[last]['SpreadPrice']
            #     list_tick_group[last]['ave_SpreadPrice'] = list_tick_group[last][
            #                                                    'sum_SpreadPrice'] / len_list_tick_group
            #     list_tick_group[last]['above_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] + band * min_move
            #     list_tick_group[last]['below_band_SpreadPrice'] = list_tick_group[last][
            #                                                           'ave_SpreadPrice'] - band * min_move
        return list_tick_group

    # 计算价差指标
    def count_indication(self, list_tick_group):
        len_list_tick_group = len(list_tick_group)
        for i in range(len_list_tick_group):
            if i >= len_average:
                list_tick_group[i]['sum_SpreadPrice'] = list_tick_group[i - 1]['sum_SpreadPrice'] + \
                                                           list_tick_group[i]['SpreadPrice'] - \
                                                           list_tick_group[i - len_average][
                                                               'SpreadPrice']
                list_tick_group[i]['ave_SpreadPrice'] = list_tick_group[i]['sum_SpreadPrice'] / len_average
                list_tick_group[i]['above_band_SpreadPrice'] = list_tick_group[i][
                                                                      'ave_SpreadPrice'] + band * min_move
                list_tick_group[i]['below_band_SpreadPrice'] = list_tick_group[i][
                                                                      'ave_SpreadPrice'] - band * min_move
            elif 0 < i < len_average:
                try:
                    list_tick_group[i]['sum_SpreadPrice'] = list_tick_group[i - 1]['sum_SpreadPrice'] + \
                                                               list_tick_group[i]['SpreadPrice']
                except:
                    print("i =", i)
                    print("list_tick_group[i-1] =", list_tick_group[i - 1])
                    print("list_tick_group[i-2] =", list_tick_group[i - 2])
                    print("list_tick_group[i] =", list_tick_group[i])
                list_tick_group[i]['ave_SpreadPrice'] = list_tick_group[i]['sum_SpreadPrice'] / (i + 1)
                list_tick_group[i]['above_band_SpreadPrice'] = list_tick_group[i][
                                                                      'ave_SpreadPrice'] + band * min_move
                list_tick_group[i]['below_band_SpreadPrice'] = list_tick_group[i][
                                                                      'ave_SpreadPrice'] - band * min_move
            elif i == 0:
                list_tick_group[i]['sum_SpreadPrice'] = list_tick_group[i]['SpreadPrice']
                list_tick_group[i]['ave_SpreadPrice'] = list_tick_group[i]['sum_SpreadPrice']
                list_tick_group[i]['above_band_SpreadPrice'] = list_tick_group[i][
                                                                      'ave_SpreadPrice'] + band * min_move
                list_tick_group[i]['below_band_SpreadPrice'] = list_tick_group[i][
                                                                  'ave_SpreadPrice'] - band * min_move
        return list_tick_group

if __name__ == '__main__':
    # 取数据的参数
    instrument_id_a = 'cu1802'
    instrument_id_b = 'cu1801'
    # 价差指标参数
    len_average = 1000  # 均值
    band = 2  # 上下轨道=n倍最小跳
    min_move = 10  # 最小跳
    sum_SpreadPrice = 0  # 价差指标求和，初始值
    ave_SpreadPrice = 0  # 价值指标求平均值，初始值；
    str_date = '20171031'  # 获取数据的日期
    # 计算出str_date的上一个交易日的日期，目标各位为'20171027'
    market_data_model = MarketDataModel('101.132.99.239',
                                        '9901',
                                        'CTP_MARKET_DATA',
                                        ':)xTrader:)admin:)',
                                        ':)&xtrader&:)')
    print(">>>start time =", datetime.datetime.now().strftime('%X'))
    list_tick_group = market_data_model.compound_tick(instrument_id_a, instrument_id_b, str_date)
    # 如果当前交易日的行情样本数据不够指标计算所需，则获取前一个交易日数据，在七天内寻找
    if len(list_tick_group) < len_average:
        print(">>>当前交易日的行情样本数不够指标所需样本数")
        # 七个自然日内有历史行情数据
        pre_tradingday = market_data_model.pre_tradingday_date(str_date)
        if pre_tradingday is not None:
            list_tick_group_pre = market_data_model.compound_tick(instrument_id_a, instrument_id_b, pre_tradingday)
            print(">>>历史交易日行情数据长度 =", len(list_tick_group_pre))
            list_tick_group = list_tick_group_pre + list_tick_group  # 结合历史行情和当前交易日行情
            print(">>>合并当天行情数据和历史行情数据之后的长度 =", len(list_tick_group_pre))
        # 七个自然日内都没有历史行情数据
        else:
            print(">>>七个自然日内都没有历史行情数据")
            pass
    else:
        print(">>>当前交易日的行情样本数足够指标所需样本数")
    list_tick_group = market_data_model.count_indication(list_tick_group)
    print(">>>len(list_tick_group) =", len(list_tick_group))

    df_tick_group = pd.DataFrame(list_tick_group)
    df_tick_group.to_csv('C:/Users/yuwangying/Desktop/tmp/df_tick_group.csv')
    print(">>>end time =", datetime.datetime.now().strftime('%X'))

