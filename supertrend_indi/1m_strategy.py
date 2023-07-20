import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta
from datetime import date
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)


def get_historical_data_from_csv(symbol, start_date):
    df = pd.read_csv(f"csv/{symbol}_M1_2008.csv")
    df = df.set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)
    return df

stock = "aapl"
tday = datetime.today()
startDay = tday - timedelta(days=100)   
# _df = pd.DataFrame() # Empty DataFrame
# df = yf.download(stock,start=startDay,end=tday)
df = get_historical_data_from_csv('XAU_USD', '2008-12-31')

df.ta.supertrend(period=7, multiplier=3)
# OR if you want to automatically apply the results to the DataFrame
df.ta.supertrend(period=7, multiplier=3, append=True)

# Get only one pattern
_doji_df = pd.DataFrame(df.ta.cdl_pattern(name="doji"))
doji_df = _doji_df.reset_index()

for i, row in doji_df.iterrows():
    if row["CDL_DOJI_10_0.1"] > 0:
        print("Index:",i, ", row:",row)

_ema_df = pd.DataFrame(ta.ema(df["close"], length=60))
ema_df = _ema_df.reset_index()

# (1) Create the Strategy
# MyStrategy = ta.Strategy(
#     name="DCSMA10",
#     ta=[
#         {"kind": "ohlc4"},
#         {"kind": "sma", "length": 10},
#         {"kind": "donchian", "lower_length": 10, "upper_length": 15},
#         {"kind": "ema", "close": "OHLC4", "length": 60, "suffix": "OHLC4"},
#     ]
# )

# # (2) Run the Strategy
# kwargs = {}
# df.ta.strategy(MyStrategy, **kwargs)

import plotly.graph_objects as go

# prepare data
g_df = df.reset_index()
# print(g_df)
fig = go.Figure(data=
                [go.Candlestick(x=g_df['datetime'],
                    open=g_df['open'],
                    high=g_df['high'],
                    low=g_df['low'],
                    close=g_df['close']
                    , line=dict(width=2)
                    ),
                ])

# ema
fig.add_trace(
    go.Scatter(mode = 'lines',
                        x=ema_df['datetime'],
                        y=ema_df['EMA_60'],
                        line={'color':'blue', 'width':1},
                        name="ema60"
                )
            )

# fig.add_trace(
#     go.Scatter(mode = 'markers',
#                         x=doji_df['datetime'],
#                         y=doji_df['CDL_DOJI_10_0.1'],
#                         line={'color':'red'},
#                         name="doji"
#                 )
#             )

fig.show()