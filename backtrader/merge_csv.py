import pandas as pd
import os
import glob

# df = pd.concat(map(pd.read_csv, glob.glob(os.path.join("XAU_USD", "*.csv"))), ignore_index= True)
start = 2008
for y in range(12):
    df = pd.read_csv(f"XAU_USD/XAU_USD_M1_{start+y}.csv")
    df["Adj Close"] = df["Close"]
    df.to_csv(f"XAU_USD/XAU_USD_M1_{start+y}.csv", index=False)
    y += 1