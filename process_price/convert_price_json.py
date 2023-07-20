import pandas as pd

file_name = "S50H2360"
df = pd.read_csv(f"dataset/{file_name}.csv", names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

#merge date + time column
df["symbol"] = "S50H23"
df["datetime"] = df[["date", "time"]].apply(" ".join, axis=1)+":00"
df["timestamp"] = (pd.to_datetime(df['datetime'],format= '%Y.%m.%d %H:%M' ).values.astype('int64') // 10 ** 9)*1000
df = df[["datetime", "timestamp", "symbol", "open", "high", "low", "close"]]

js = df.to_json(orient="records", indent=4)

f = open(f"output/{file_name}.json", "a")
f.write(js)
f.close()
