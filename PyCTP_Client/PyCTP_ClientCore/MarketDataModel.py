import queue
import urllib.parse
from pymongo import MongoClient
from sys import getsizeof
import datetime
import pandas


# 生成group_tick
def transform_tick_group(instrument_id_a, instrument_id_b, tick, tick_group):
    # 标明tick_group中存在的合约行情
    if tick_group is None:
        tick_group = dict()
        if tick['InstrumentID'] == instrument_id_a:
            tick_group['InstrumentExist'] = 'Ab'
        if tick['InstrumentID'] == instrument_id_b:
            tick_group['InstrumentExist'] = 'aB'
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
        tick_group['UpdateMillisec_a'] = tick['UpdateMillisec']
        tick_group['UpdateTime_a'] = tick['UpdateTime']
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
        tick_group['UpdateMillisec_b'] = tick['UpdateMillisec']
        tick_group['UpdateTime_b'] = tick['UpdateTime']
        tick_group['TradingDay'] = tick['TradingDay']
    return tick_group


class MarketDataModel():
    # 创建一个具有maximum_connections的mongodb带权限验证的连接池
    # ipaddr => mongodb server ip
    # port => mongod server port
    # dbname => mongodb database name
    # name => mongodb name of user
    # pwd => mongodb password of user
    # collection_name => the collection_name you want to operate
    def __init__(self, ipaddr, port, dbname, name, pwd, collection_name):
        # 创建连接
        username = urllib.parse.quote_plus(name)
        password = urllib.parse.quote_plus(pwd)
        uri = "mongodb://" + username + ":" + password + "@" + ipaddr + ":" + str(port) + "/admin?authMechanism=SCRAM-SHA-1"
        self.client = MongoClient(uri)  # 连接实例
        self.db = self.client[dbname]  # 数据库链接
        self.col_op = self.db[collection_name]  # 集合链接
        # self.col_op.create_index("InstrumentID", background=True)  # 创建索引
        # self.col_op.drop_indexes()
        print(">>>MarketDataModel.__init__() finished")

if __name__ == '__main__':
    market_data_model = MarketDataModel('101.132.99.239',
                                        '9901',
                                        'CTP_MARKET_DATA',
                                        ':)xTrader:)admin:)',
                                        ':)&xtrader&:)',
                                        '20170927')
    projection_filter = {"_id": 0,
                         "InstrumentID": 1,
                         "LastPrice": 1,
                         "Volume": 1,
                         "AskPrice1": 1,
                         "BidPrice1": 1,
                         "AskVolume1": 1,
                         "BidVolume1": 1,
                         "UpdateTime": 1,
                         "UpdateMillisec": 1,
                         "OpenPrice": 1,
                         "HighestPrice": 1,
                         "TradingDay": 1,
                         "UpperLimitPrice": 1,
                         "LowerLimitPrice": 1
                         }
    print("start", datetime.datetime.now().strftime('%X'))
    data_cursor = market_data_model.col_op.find(filter={'InstrumentID': {"$in": ['rb1801', 'rb1805']}},
                                                # projection=projection_filter,
                                                projection={'_id': 0},
                                                no_cursor_timeout=True)
    # print(">>>MarketDataModel.main() data_cursor =", data_cursor)

    list_tick_group = list()
    instrument_id_a = 'rb1805'
    instrument_id_b = 'rb1801'
    for tick in data_cursor:
        len_list_tick_group = len(list_tick_group)
        if len_list_tick_group > 0:
            # 最新tick合约代码存在于最后一条tick_group中，则将最新tick存入到新加入行
            if tick['InstrumentID'] in list_tick_group[len_list_tick_group]:
                tick_group = transform_tick_group(instrument_id_a, instrument_id_b, tick, None)
                list_tick_group[i] = tick_group
            # 最新tick合约代码不存在于最后一条tick_group中
            elif tick['InstrumentID'] not in list_tick_group[i]:
                # 判断合约id，已存在与tick_group中的行情键名
                if tick['InstrumentID'] == instrument_id_a:
                    update_time = 'UpdateTime_b'
                    update_millisec = 'UpdateMillisec_b'
                elif tick['InstrumentID'] == instrument_id_b:
                    update_time = 'UpdateTime_a'
                    update_millisec = 'UpdateMillisec_a'

                # 最新tick的行情时间等于最后一条tick_group中已经存在的另外一个合约的行情时间，则合并在tick_group最后一行
                if tick['UpdateTime'] == list_tick_group[i][update_time] \
                        and tick['UpdateMillisec'] == list_tick_group[i][update_millisec]:
                    pass
                # 最新tick的行情时间小于最后一条tick_group中已经存在的行情时间
                elif tick['UpdateTime'] < list_tick_group[i][update_time] \
                        or tick['UpdateTime'] == list_tick_group[i][update_time] \
                                and tick['UpdateMillisec'] < list_tick_group[i][update_millisec]:
                    # 特殊情况：换了自然日，最新tick更新时间是00:00:00之后，最后一条tick_group更新时间是23:59:59
                    if '21:00:00' <= list_tick_group[i][update_time] and list_tick_group[i][update_time] <= '23:59:59' \
                            and '00:00:00' <= tick['UpdateTime'] and tick['UpdateTime'] <= '15:00:00':
                        i = i + 1
                        if tick['InstrumentID'] == instrument_id_a:
                            tick_group = {
                                'InstrumentID_a': tick['InstrumentID'],
                                'LastPrice_a': tick['LastPrice'],
                                'AskPrice1_a': tick['AskPrice1'],
                                'AskVolume1_a': tick['AskVolume1'],
                                'BidPrice1_a': tick['AskPrice1'],
                                'BidVolume1_a': tick['BidVolume1'],
                                'UpperLimitPrice_a': tick['UpperLimitPrice'],
                                'LowerLimitPrice_a': tick['LowerLimitPrice'],
                                'OpenInterest_a': tick['OpenInterest'],
                                'Volume_a': tick['Volume'],
                                'UpdateMillisec_a': tick['UpdateMillisec'],
                                'UpdateTime_a': tick['UpdateTime'],
                                'TradingDay': tick['TradingDay'],
                            }
                        elif tick['InstrumentID'] == instrument_id_b:
                            tick_group = {
                                'InstrumentID_b': tick['InstrumentID'],
                                'LastPrice_b': tick['LastPrice'],
                                'AskPrice1_b': tick['AskPrice1'],
                                'AskVolume1_b': tick['AskVolume1'],
                                'BidPrice1_b': tick['AskPrice1'],
                                'BidVolume1_b': tick['BidVolume1'],
                                'UpperLimitPrice_b': tick['UpperLimitPrice'],
                                'LowerLimitPrice_b': tick['LowerLimitPrice'],
                                'OpenInterest_b': tick['OpenInterest'],
                                'Volume_b': tick['Volume'],
                                'UpdateMillisec_b': tick['UpdateMillisec'],
                                'UpdateTime_b': tick['UpdateTime'],
                                'TradingDay': tick['TradingDay'],
                            }
                    # 其他情况：错误时序数据，不处理
                    else:
                        pass
                # 最新tick的行情时间大于最后一条tick_group中已经存在的行情时间
                elif tick['UpdateTime'] > list_tick_group[i][update_time] \
                        or tick['UpdateTime'] == list_tick_group[i][update_time] \
                                and tick['UpdateMillisec'] > list_tick_group[i][update_millisec]:
                    pass
        elif len_list_tick_group == 0:
            tick_group = transform_tick_group(instrument_id_a, instrument_id_b, tick, None)
            # if tick['InstrumentID'] == instrument_id_a:
            #     tick_group = {
            #        'InstrumentID_a': tick['InstrumentID'],
            #        'LastPrice_a': tick['LastPrice'],
            #        'AskPrice1_a': tick['AskPrice1'],
            #        'AskVolume1_a': tick['AskVolume1'],
            #        'BidPrice1_a': tick['AskPrice1'],
            #        'BidVolume1_a': tick['BidVolume1'],
            #        'UpperLimitPrice_a': tick['UpperLimitPrice'],
            #        'LowerLimitPrice_a': tick['LowerLimitPrice'],
            #        'OpenInterest_a': tick['OpenInterest'],
            #        'Volume_a': tick['Volume'],
            #        'UpdateTime_a': tick['UpdateTime'],
            #        'UpdateMillisec_a': tick['UpdateMillisec'],
            #        'TradingDay': tick['TradingDay'],
            #     }
            # elif tick['InstrumentID'] == instrument_id_b:
            #     tick_group = {
            #        'InstrumentID_b': tick['InstrumentID'],
            #        'LastPrice_b': tick['LastPrice'],
            #        'AskPrice1_b': tick['AskPrice1'],
            #        'AskVolume1_b': tick['AskVolume1'],
            #        'BidPrice1_b': tick['AskPrice1'],
            #        'BidVolume1_b': tick['BidVolume1'],
            #        'UpperLimitPrice_b': tick['UpperLimitPrice'],
            #        'LowerLimitPrice_b': tick['LowerLimitPrice'],
            #        'OpenInterest_b': tick['OpenInterest'],
            #        'Volume_b': tick['Volume'],
            #        'UpdateMillisec_b': tick['UpdateMillisec'],
            #        'UpdateTime_b': tick['UpdateTime'],
            #        'TradingDay': tick['TradingDay'],
            #     }
            list_tick_group[i] = tick_group

    print("transform to list finished", datetime.datetime.now().strftime('%X'))
    df_data = pandas.DataFrame(list_tick_group)
    print(">>> df_data.count =", df_data.count())
    df_filtered = df_data.query("UpdateTime>='21:00:00' and UpdateTime<='23:00:00' or UpdateTime>='09:00:00' and UpdateTime<='15:00:00'")
    print(">>> df_filtered.count =", df_filtered.count())
    print("transform to list DataFrame finished", datetime.datetime.now().strftime('%X'))
    df_data.to_csv('D:/CTP_Dev/数据样本/CTP/df_data.csv')
    df_filtered.to_csv('D:/CTP_Dev/数据样本/CTP/df_filtered.csv')
    print("save data to local finished", datetime.datetime.now().strftime('%X'))
    print("end", datetime.datetime.now().strftime('%X'))

