import yfinance as yf
import datetime
import pandas_ta as ta
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def calculate_swings_with_trend_conditions(prices):
    swings = []
    prev_price = prices[0]
    swing_start = prev_price
    swing_duration = 0
    
    # Calculate Hull Moving Averages (HMA) for 14 and 60 periods
    hma_14 = ta.hma(prices, length=50)
    hma_60 = ta.hma(prices, length=100)
    
    # Calculate Relative Strength Index (RSI)
    rsi = ta.rsi(prices)
    
    for i in range(1, len(prices)):
        price = prices[i]
        hma14 = hma_14[i]
        hma60 = hma_60[i]
        rsi_value = rsi[i]
        
        # Check for trend conditions
        if hma14 > hma60 and rsi_value > 50:  # Up trend condition
            if price > prev_price:  # Increasing price (low to high)
                if swing_duration > 0:
                    swings.append((swing_start, prev_price, swing_duration))
                swing_start = prev_price
                swing_duration = 0
        elif hma14 < hma60 and rsi_value < 50:  # Down trend condition
            if price < prev_price:  # Decreasing price (high to low)
                if swing_duration > 0:
                    swings.append((swing_start, prev_price, swing_duration))
                swing_start = prev_price
                swing_duration = 0
        
        swing_duration += 1
        prev_price = price
    
    # Calculate average swing price
    total_swing_prices = sum([(high - low) for low, high, _ in swings])
    average_swing_price = total_swing_prices / len(swings) if len(swings) > 0 else 0
    
    # Calculate average swing period
    total_swing_periods = sum([duration for _, _, duration in swings])
    average_swing_period = total_swing_periods / len(swings) if len(swings) > 0 else 0
    
    return swings, average_swing_price, average_swing_period

# Define the symbol for GBP/USD
symbol = "GBPUSD=X"  # Symbol for GBP/USD on Yahoo Finance

# Define the date range for the last 3 months
# end_date = datetime.datetime.today()
# start_date = end_date - datetime.timedelta(days=90)  # 90 days is approximately 3 months

# Fetch historical price data
# historical_data = yf.download(symbol, start=start_date, end=end_date, interval="1m")["Close"]
historical_data = pd.read_csv("../../get_price/price_datas/GBP_USD/M1/GBP_USD_M1_2022-3MNTH.csv")["Close"]

# Calculate average swing price and average swing period considering trend conditions
swings, average_swing_price, average_swing_period = calculate_swings_with_trend_conditions(historical_data)

print(f"Average Swing Price: {average_swing_price}")
print(f"Average Swing Period: {average_swing_period:.2f} minutes")

# fig = px.bar(average_swing_price)
# fig.write_html('first_figure.html', auto_open=True)

plt.plot(swings)
plt.ylabel('average_swing_price')
plt.show()