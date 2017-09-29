import queue
import urllib.parse
from pymongo import MongoClient
from sys import getsizeof
import datetime
import pandas
import numpy as np


# 目标df数据分析
def df_count(df):
    print(">>>df_count() called")
    return df


class MarketDataModel():
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
        print(">>>AccountAnalysis.__init__() finished")

if __name__ == '__main__':
    market_data_model = MarketDataModel('101.132.99.239',
                                        '9901',
                                        'CTP',  # 数据库名
                                        ':)xTrader:)admin:)',
                                        ':)&xtrader&:)',
                                        'tradingaccount'  # 集合名
                                        )
    # 文档过滤条件
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
    print(">>>main() start time =", datetime.datetime.now().strftime('%X'))
    data_cursor = market_data_model.col_op.find(
        # filter={'InstrumentID': {"$in": ['rb1801', 'rb1805']}},
        # projection=projection_filter,
        projection={'_id': 0},
        no_cursor_timeout=True
    )
    list_data = list()
    for doc in data_cursor:
        list_data.append(doc)
    df_data = pandas.DataFrame(list_data)
    array_accout = np.unique(df_data[['AccountID']].values)  # 选出期货账户
    writer = pandas.ExcelWriter('C:/Users/yuwangying/Desktop/tmp/AccountAnalysis/AccountAnalysis.xlsx')  # 创建xlsx写文件实例
    for account_id in array_accout:
        df_filtered = df_data.loc[df_data['AccountID'] == account_id]
        df_analysis = df_count(df_filtered)
        df_analysis.to_excel(excel_writer=writer,
                             sheet_name=account_id
                             )
    df_data.to_excel(excel_writer=writer,
                     sheet_name='all_account'
                     )
    writer.save()  # 保存xlsx文件
    # df数据过滤
    # df_filtered = df_data.query("UpdateTime>='21:00:00' and UpdateTime<='23:00:00' or UpdateTime>='09:00:00' and UpdateTime<='15:00:00'")
    print(">>>main() end time =", datetime.datetime.now().strftime('%X'))

