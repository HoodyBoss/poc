import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from math import floor
from termcolor import colored as cl

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

# Plot candlestick chart
def plot_candlestick():
    #create DataFrame
    prices = pd.DataFrame({'open': [25, 22, 21, 19, 23, 21, 25, 29],
                        'close': [24, 20, 17, 23, 22, 25, 29, 31],
                        'high': [28, 27, 29, 25, 24, 26, 31, 37],
                        'low': [22, 16, 14, 17, 19, 18, 22, 26]},
                        index=pd.date_range("2021-01-01", periods=8, freq="d"))

    #create figure
    plt.figure()

    #define width of candlestick elements
    width = .4
    width2 = .05

    #define up and down prices
    up = prices[prices.close>=prices.open]
    down = prices[prices.close<prices.open]

    #define colors to use
    col1 = 'green'
    col2 = 'red'

    #plot up prices
    plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
    plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
    plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

    #plot down prices
    plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
    plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
    plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    #display candlestick chart
    plt.show()

# plot_candlestick()
# EXTRACTING DATA

def get_historical_data_from_csv(symbol, start_date):
    df = pd.read_csv(f"csv/{symbol}_M1_2008.csv")
    # df.reset_index()
    df = df.set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)
    return df

def get_historical_data(symbol, start_date):
    api_key = 'bac62cf269fa4365a0b3f12632fcf01b'
    api_url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=5000&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df['values']).iloc[::-1].set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)
    return df

# tsla = get_historical_data('XAU/USD', '2023-05-28')
tsla = get_historical_data_from_csv('XAU_USD', '2008-12-01')
print(tsla)
# SUPERTREND CALCULATION
def get_supertrend(high, low, close, lookback, multiplier):
    
    # ATR
    
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(lookback).mean()
    
    # H/L AVG AND BASIC UPPER & LOWER BAND
    
    hl_avg = (high + low) / 2
    upper_band = (hl_avg + multiplier * atr).dropna()
    lower_band = (hl_avg - multiplier * atr).dropna()
    
    # FINAL UPPER BAND
    
    final_bands = pd.DataFrame(columns = ['upper', 'lower'])
    final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
    final_bands.iloc[:,1] = final_bands.iloc[:,0]
    
    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i,0] = 0
        else:
            if (upper_band[i] < final_bands.iloc[i-1,0]) | (close[i-1] > final_bands.iloc[i-1,0]):
                final_bands.iloc[i,0] = upper_band[i]
            else:
                final_bands.iloc[i,0] = final_bands.iloc[i-1,0]
    
    # FINAL LOWER BAND
    
    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i, 1] = 0
        else:
            if (lower_band[i] > final_bands.iloc[i-1,1]) | (close[i-1] < final_bands.iloc[i-1,1]):
                final_bands.iloc[i,1] = lower_band[i]
            else:
                final_bands.iloc[i,1] = final_bands.iloc[i-1,1]
    
    # SUPERTREND
    
    supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
    supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
    
    for i in range(len(supertrend)):
        if i == 0:
            supertrend.iloc[i, 0] = 0
        elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] < final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] > final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] > final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] < final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
    
    supertrend = supertrend.set_index(upper_band.index)
    supertrend = supertrend.dropna()[1:]
    
    # ST UPTREND/DOWNTREND
    
    upt = []
    dt = []
    close = close.iloc[len(close) - len(supertrend):]

    for i in range(len(supertrend)):
        if close[i] > supertrend.iloc[i, 0]:
            upt.append(supertrend.iloc[i, 0])
            dt.append(np.nan)
        elif close[i] < supertrend.iloc[i, 0]:
            upt.append(np.nan)
            dt.append(supertrend.iloc[i, 0])
        else:
            upt.append(np.nan)
            dt.append(np.nan)
            
    st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
    upt.index, dt.index = supertrend.index, supertrend.index
    
    return st, upt, dt

tsla['st'], tsla['s_upt'], tsla['st_dt'] = get_supertrend(tsla['high'], tsla['low'], tsla['close'], 10, 3)
tsla = tsla[1:]
print(tsla.head())

# SUPERTREND PLOT

# plt.plot(tsla['close'], linewidth = 2, label = 'CLOSING PRICE')
# plt.plot(tsla['st'], color = 'green', linewidth = 2, label = 'ST UPTREND 10,3')
# plt.plot(tsla['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND 10,3')
# plt.legend(loc = 'upper left')
# plt.show()

# SUPERTREND STRATEGY

def implement_st_strategy(prices, st):
    buy_price = []
    sell_price = []
    st_signal = []
    signal = 0
    
    for i in range(len(st)):
        # print("Implement st strategy : st i-1:", st[i-1], ', price [i-1]: ',prices[i-1], ', st[i]:', st[i] , ', price[i]:')
        if st[i-1] > prices[i-1] and st[i] < prices[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                st_signal.append(signal)
                # print("Buyyyyyyyyyy !!!!!!!!! Yes ")
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                st_signal.append(0)
        elif st[i-1] < prices[i-1] and st[i] > prices[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                st_signal.append(signal)
                # print("Sellllllllll >>>>>>>>>>>>>> Yes ")?
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                st_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            st_signal.append(0)
        
        
    return buy_price, sell_price, st_signal

buy_price, sell_price, st_signal = implement_st_strategy(tsla['close'], tsla['st'])

buy_df = pd.DataFrame(buy_price,columns=["buy_price"])
sell_df = pd.DataFrame(sell_price,columns=["sell_price"])
signal_df = pd.DataFrame(st_signal,columns=["signal"])
final_data = {"buy_price": buy_price,
              "sell_price": sell_price,
               "signal": st_signal }

final_df = pd.DataFrame(final_data)

# print("$"*100)
# for index, row in final_df.iterrows():
#     if row["buy_price"] > 0:
#         print("buy index:",index, ", data:", row["buy_price"] , row["signal"])
    
#     if row["sell_price"] > 0:
#         print("sell index:",index, ", data:", row["sell_price"] , row["signal"])

# SUPERTREND SIGNALS
# ii = 0
# for index, rec in tsla.iterrows():
#     plt.plot(rec['close'], linewidth = 2)
#     plt.plot(rec['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
#     plt.plot(rec['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
#     plt.plot(index, buy_price[ii], marker = '^', color = 'green', markersize = 12, linewidth = 0, label = 'BUY SIGNAL')
#     plt.plot(index, sell_price[ii], marker = 'v', color = 'r', markersize = 12, linewidth = 0, label = 'SELL SIGNAL')
#     plt.pause(0.05)
#     ii += 1

## Plot graph whole of data
plt.plot(tsla['close'], linewidth = 2)
plt.plot(tsla['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
plt.plot(tsla['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
plt.plot(tsla.index, buy_price, marker = '^', color = 'green', markersize = 12, linewidth = 0, label = 'BUY SIGNAL')
plt.plot(tsla.index, sell_price, marker = 'v', color = 'r', markersize = 12, linewidth = 0, label = 'SELL SIGNAL')
plt.title('GOLD ST TRADING SIGNALS')
plt.legend(loc = 'upper left')
plt.show()

# GENERATING STOCK POSITION
# print("<"*40, " St Signal ", ">"*40)
position = []
for i in range(len(st_signal)):
    # print(f"St sig:{i}, val:{st_signal[i]}")
    if st_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)


buy_flag = False
for i in range(len(tsla['close'])):
    if st_signal[i] == 1:
        position[i] = 1
        buy_flag = True
    elif st_signal[i] == -1:
        position[i] = 0
        buy_flag = False
    else:
        if buy_flag:
            position[i] = 1 #position[i-1] + 1
        else:
            position[i] = 0


close_price = tsla['close']
st = tsla['st']
st_signal = pd.DataFrame(st_signal).rename(columns = {0:'st_signal'}).set_index(tsla.index)
position = pd.DataFrame(position).rename(columns = {0:'st_position'}).set_index(tsla.index)
print(">"*40, " Position ", ">"*40)
print(position.iloc[100:110])

frames = [close_price, st, st_signal, position]
strategy = pd.concat(frames, join = 'inner', axis = 1)

strategy.head()
# print(">"*40, " Strategy with close diff ", ">"*40)
# c_diff = np.diff(strategy["close"])
# print( strategy.iloc[100:105] )
# BACKTESTING
tsla_ret = pd.DataFrame(np.diff(tsla['close'])).rename(columns = {0:'returns'})
st_strategy_ret = []

# print(">"*40, " Return ", ">"*40)
# print(tsla_ret[100:105])

for i in range(len(tsla_ret)):
    returns = tsla_ret['returns'][i]*strategy['st_position'][i]
    st_strategy_ret.append(returns)
    
print(">"*40, " Strategy Return ", ">"*40)

st_strategy_ret_df = pd.DataFrame(st_strategy_ret).rename(columns = {0:'st_returns'})
print( st_strategy_ret_df.iloc[100:105] )

investment_value = 100000
number_of_stocks = 100 #floor(investment_value/tsla['close'][-1])
st_investment_ret = []

for i in range(len(st_strategy_ret_df['st_returns'])):
    returns = number_of_stocks*st_strategy_ret_df['st_returns'][i]
    st_investment_ret.append(returns)

st_investment_ret_df = pd.DataFrame(st_investment_ret).rename(columns = {0:'investment_returns'})
total_investment_ret = round(sum(st_investment_ret_df['investment_returns']), 2)
profit_percentage = floor((total_investment_ret/investment_value)*100)
print(cl('Profit gained from the ST strategy by investing $100k in GOLD : {}'.format(total_investment_ret), attrs = ['bold']))
print(cl('Profit percentage of the ST strategy : {}%'.format(profit_percentage), attrs = ['bold']))
# SPY ETF COMPARISON
def get_benchmark(start_date, investment_value):
    spy = get_historical_data('SPY', start_date)['close']
    benchmark = pd.DataFrame(np.diff(spy)).rename(columns = {0:'benchmark_returns'})
    
    investment_value = investment_value
    number_of_stocks = floor(investment_value/spy[-1])
    benchmark_investment_ret = []
    
    for i in range(len(benchmark['benchmark_returns'])):
        returns = number_of_stocks*benchmark['benchmark_returns'][i]
        benchmark_investment_ret.append(returns)

    benchmark_investment_ret_df = pd.DataFrame(benchmark_investment_ret).rename(columns = {0:'investment_returns'})
    return benchmark_investment_ret_df

benchmark = get_benchmark('2008-12-01', 100000)
investment_value = 100000
total_benchmark_investment_ret = round(sum(benchmark['investment_returns']), 2)
benchmark_profit_percentage = floor((total_benchmark_investment_ret/investment_value)*100)
print('*'*200)
print(cl('Benchmark profit by investing $100k : {}'.format(total_benchmark_investment_ret), attrs = ['bold']))
print(cl('Benchmark Profit percentage : {}%'.format(benchmark_profit_percentage), attrs = ['bold']))
print(cl('ST Strategy profit is {}% higher than the Benchmark Profit'.format(profit_percentage - benchmark_profit_percentage), attrs = ['bold']))