import pandas as pd
import numpy as np

symbol = "GBP_JPY"
year = "2023"
tf = "M1"
max_order = 5
min_point_value_step = 0.001
pip_value = 0.07
point_value = pip_value/10
# Assuming you have your price data loaded into 'historical_data'
historical_data = pd.read_csv(f"../../get_price/price_datas/{symbol}/{tf}/{symbol}_{tf}_{year}.csv")

historical_data['DateTime'] = pd.to_datetime(historical_data['Datetime'])

# Truncate the 'DateTime' column to date only
historical_data['DateOnly'] = historical_data['DateTime'].dt.date

# Set the window size for daily analysis (e.g., 1440 minutes in a day)
# original hist price data is timeframe 1m
# window in 1 day
window_size_mp = 1 # 1 = 1 day, 0.5 = half day
window_size = int(round(window_size_mp*1440,0))

# Calculate daily swings based on minimum and maximum values in each window
daily_swings = []
swing_prices = {}
for i in range(0, len(historical_data), window_size):
    window_data = historical_data[i:i + window_size]
    
    # min_price = np.min(window_data['Close'])
    # max_price = np.max(window_data['Close'])
    
    min_price_df = window_data[window_data['Close'] == window_data['Close'].min()]
    max_price_df = window_data[window_data['Close'] == window_data['Close'].max()]
    min_price = min_price_df.iloc[0]["Close"]
    max_price = max_price_df.iloc[0]["Close"]
    
    start_date = max_price_df.iloc[0]["DateOnly"]
    # print(f"Date:{start_date}, min:{min_price_df.iloc[0]}, max:{max_price_df.iloc[0]}")
    swing_price = max_price - min_price

    daily_swings.append(swing_price)
    swing_prices.update({str(swing_price): {"at_date": start_date, "min": min_price, "max": max_price}})

# Calculate the average swing price
with open('swing_price.csv', 'w') as f:
    f.write(f"swing price,date,min,max"+"\n")
    for x in swing_prices:
        f.write(x+","+str(swing_prices[x]["at_date"])+","+str(swing_prices[x]["min"])+","+str(swing_prices[x]["max"])+"\n")
    f.close()    

average_swing_price = np.mean(daily_swings)
min_swing_price = np.min(daily_swings)
max_swing_price = np.max(daily_swings)

print(f"Average Swing Price: {average_swing_price}")
print(f"Min Price: {swing_prices[str(max_swing_price)]['min']}, Max Price: {swing_prices[str(max_swing_price)]['max']} at {swing_prices[str(max_swing_price)]['at_date']}")
print(f"Min Swing Price: {min_swing_price}, Max Swing Price: {max_swing_price}")
print(f"Min Swing Point: {min_swing_price/min_point_value_step}, Max Swing Point: {max_swing_price/min_point_value_step}")
print(f"Min Swing Value 1 order: ${(min_swing_price/min_point_value_step)*point_value}, Max Swing Value 1 order: ${(max_swing_price/min_point_value_step)*point_value}")
print(f"Min Swing Value {max_order} order(s): ${(min_swing_price/min_point_value_step)*point_value*max_order}, Max Swing Value {max_order} order(s): ${(max_swing_price/min_point_value_step)*point_value*max_order}")
