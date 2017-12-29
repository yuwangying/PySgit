import urllib.parse
from pymongo import MongoClient
import datetime
import pandas
import numpy as np
# import math
# import queue
# from sys import getsizeof


# 新增列：手续费返还累积
def count_commission_accumulate(df):
    for index, row in df.iterrows():
        print(">>>count_commission_accumulate", row['TradingDay'], row['Available'])
    return df


# 目标df数据分析
def df_count(df):
    # 净平仓盈亏 = 平仓盈亏 - 手续费
    df['NetCloseProfit'] = df.apply(lambda row: row.CloseProfit - row.Commission, axis=1)
    # 手续费返还金额 = 手续费 * (1/1.1) * 0.4 * 0.7
    df['CommissionReturn'] = df.apply(lambda row: row.Commission * 0.25454545, axis=1)
    # 手续费返还累积
    df['CommissionReturnAccumulate'] = df['CommissionReturn'].cumsum()
    # 风险度 = 占用保证金 / (占用保证金 + 可用资金)
    df['RsikRatio'] = df.apply(lambda row: row.CurrMargin / (row.CurrMargin + row.Available), axis=1)
    # 动态权益 = 占用保证金 + 可用资金
    df['ActiveDeposit'] = df.apply(lambda row: row.Available + row.CurrMargin, axis=1)
    # 昨日动态权益
    df['PreActiveDeposit'] = df['ActiveDeposit'].shift() if np.isnan(df['ActiveDeposit'].shift()) is not True else df['ActiveDeposit']
    # 动态权益变化 = 今日动态权益 - 昨日动态权益 + 出金 - 入金
    df['ActiveDepositChange'] = df['ActiveDeposit'] - df['PreActiveDeposit'] + df['Withdraw'] - df['Deposit']
    # 动态权益收益率 = 昨日动态权益 + 入金
    df['ActiveDepositRateOfReturn'] = df['ActiveDepositChange'] / (df['ActiveDeposit'] + df['Withdraw'])
    # 动态权益变化累积
    df['ActiveDepositChangeAccumulate'] = df['ActiveDepositChange'].cumsum()
    # 当日全部净盈亏 =  当日动态权益较静态权益变化 + 手续费返还
    df['NetTotalProfit'] = df.apply(lambda row: row.ActiveDepositChange + row.CommissionReturn, axis=1)
    # 当日全部净盈亏累积
    df['NetTotalProfitAccumulate'] = df['NetTotalProfit'].cumsum()
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
        print(">>account_id =", account_id)
        # 过滤出单个期货账号的每日账户资金记录
        df_filtered = df_data.loc[df_data['AccountID'] == account_id]
        # list_index = list(range(len(df_filtered) - 1))
        # print(list_index)
        # df_filtered.set_index(list_index)
        # 单个期货账号每日资金数据分析
        df_analysis = df_count(df_filtered)
        # 单期货账号统计后的数据保存为excel的sheet
        df_analysis.to_excel(excel_writer=writer,
                             sheet_name=account_id
                             )
    df_analysis = df_count(df_data)
    df_data.to_excel(excel_writer=writer,
                     sheet_name='all_account'
                     )
    writer.save()  # 保存xlsx文件
    # df数据过滤
    # df_filtered = df_data.query("UpdateTime>='21:00:00' and UpdateTime<='23:00:00' or UpdateTime>='09:00:00' and UpdateTime<='15:00:00'")
    print(">>>main() end time =", datetime.datetime.now().strftime('%X'))

