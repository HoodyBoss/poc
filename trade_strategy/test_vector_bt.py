import numpy as np
import pandas as pd
import vectorbt as vbt

# Placeholder function for fetching historical data
def get_historical_data():

    # Generate example historical data
    np.random.seed(42)
    n = 1000
    dates = pd.date_range(start="2022-01-01", periods=n, freq='D')
    close_prices = np.random.randint(50, 150, size=n) + np.random.randn(n) * 5
    high_prices = close_prices + np.random.randint(1, 10, size=n)
    low_prices = close_prices - np.random.randint(1, 10, size=n)
    open_prices = np.random.choice([close_prices[0], close_prices[-1]], size=n)

    # Create a DataFrame for historical data
    historical_data = pd.DataFrame({
        'Date': dates,
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices
    })
    historical_data.set_index('Date', inplace=True)
    return historical_data

# Define the scalping strategy
def scalping_strategy(close, fast_window=5, slow_window=20):
    # Calculate moving averages
    fast_sma = close.rolling(window=fast_window).mean()
    slow_sma = close.rolling(window=slow_window).mean()

    # Generate signals
    signal_long = fast_sma > slow_sma
    signal_short = fast_sma < slow_sma

    return signal_long, signal_short

if __name__ == "__main__":
    # Load historical data
    historical_data = get_historical_data()  # Replace with your data loading logic

    # Prepare the data
    close = historical_data['Close']

    # Create signals using the scalping strategy
    signal_long, signal_short = scalping_strategy(close)

    # Simulate the strategy and run the backtest
    pf = vbt.Portfolio.from_signals(close, signal_long, signal_short, init_cash=100000)

    # Print the backtest results
    print(pf.stats())
