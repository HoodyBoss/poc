import numpy as np
import pandas as pd

# Placeholder function for interacting with historical data
def get_historical_data():
    # Replace this with actual code to load historical data
    # Example: Load a CSV file or fetch data from a database
    pass

# Simple moving average calculation
def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

# Scalping backtesting function
def backtest_scalping_strategy(data, fast_window=5, slow_window=20):
    # Calculate moving averages
    data['FastSMA'] = calculate_sma(data, fast_window)
    data['SlowSMA'] = calculate_sma(data, slow_window)

    positions = []  # Keep track of positions (buy/sell signals)
    balance = 100000  # Starting balance

    for i in range(len(data)):
        if i >= slow_window:
            # Check for a crossover (buy signal)
            if data['FastSMA'][i] > data['SlowSMA'][i]:
                balance -= data['Close'][i]  # Buy at closing price
                positions.append(('buy', data.index[i], data['Close'][i]))

            # Check for a crossover (sell signal)
            elif data['FastSMA'][i] < data['SlowSMA'][i] and positions:
                balance += data['Close'][i]  # Sell at closing price
                positions.append(('sell', data.index[i], data['Close'][i]))

    return balance, positions

# Main function for backtesting
if __name__ == "__main__":
    # Load historical data
    historical_data = get_historical_data()  # Replace with your data loading logic

    # Run backtest
    final_balance, positions = backtest_scalping_strategy(historical_data)

    # Print results
    print("Final Balance:", final_balance)
    print("Number of Trades:", len(positions))
    print("Trade Details:")
    for trade in positions:
        print(trade)
