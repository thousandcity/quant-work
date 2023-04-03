# -*- coding: utf-8 -*-

import backtrader as bt
import tushare as ts
import pandas as pd
from datetime import datetime
from matplotlib.dates import DateFormatter, AutoDateLocator

# 设置tushare token
ts.set_token('ed2c66124b2b93a37a4d26e64a51379572be60acf762ed3960d7d799')

# 初始化tushare pro api
pro = ts.pro_api()


# 一个简单的策略：如果 收盘价 大于24日均线，则 buy；如果收盘价小于24日均线，则sell
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.MovingAverageSimple(self.data, period=24)

    def next(self):
        # 收盘价大于sma，买入
        if self.data.close > self.sma[0]:
            self.buy()

        # 收盘价小于等于sma，卖出
        if self.data.close <= self.sma[0]:
            self.sell()

    def stop(self):
        pass


# 数据调取
# 获取603335股票的历史日线数据
df = pro.daily(ts_code='603335.SH', start_date='20100101', end_date='20230331')
df.columns = ['stock', 'datetime', 'open', 'high', 'low', 'close', 'price', 'change', 'chg', 'volume', 'amount']
df.to_csv('603335.SH.csv', columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])

print(df)
# 将数据加载到backtrader中
# 由于trade_date是字符串，BackTrader无法识别，需要转一下
st_date = datetime(2010, 1, 1)
end_date = datetime(2023, 3, 31)
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
data = bt.feeds.PandasData(dataname=df)

# 初始化cerebro引擎
cerebro = bt.Cerebro()

# 添加数据到cerebro引擎
cerebro.adddata(data)

# 添加策略到cerebro引擎
cerebro.addstrategy(MyStrategy)

# 运行回测
cerebro.run()


# 设置日期格式
date_format = '%Y-%m-%d'
date_formatter = DateFormatter(date_format)

# 设置定位器
date_locator = AutoDateLocator()
# 可视化结果
cerebro.plot()
