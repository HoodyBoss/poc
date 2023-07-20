import pandas as pd
import pandas_ta as ta

data = pd.read_csv('XAU_USD_M1_2008.csv')

data['ma'] = ta.sma(close=data['close'], length=14, append=True)  # 20-day simple moving average
data['rsi'] = ta.rsi(close=data['close'], append=True)  # RSI indicator

data['long_signal'] = 0
data['short_signal'] = 0
data.loc[(data['close'] > data['ma']) & (data['rsi'] > 60), 'long_signal'] = 1  # Long signal when price crosses above MA and RSI > 50
data.loc[(data['close'] < data['ma']) & (data['rsi'] < 40), 'short_signal'] = -1  # Short signal when price crosses above MA and RSI > 50

data['returns'] = data['close'].pct_change()

data['long_strategy_returns'] = data['long_signal'].shift(1) * data['returns']
data['short_strategy_returns'] = data['short_signal'].shift(1) * data['returns']

long_sum = data["long_strategy_returns"]
short_sum = data["short_strategy_returns"]

data.to_csv("return.csv")
print(long_sum.sum())
print(short_sum.sum())