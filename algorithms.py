import csv

def data_processing(filepath):
    stock_history = {}
    with open(filepath, mode = "r", encoding = "utf-8") as file:
        dict_reader = csv.DictReader(file)
        if "Name" not in dict_reader.fieldnames:
            raise Exception("No Name column in CSV file. Please check the data format.")
        for row in dict_reader:
            ticker = row["Name"]
            date = row["date"]
            try:
                close_price = float(row["close"])
            except ValueError:
                continue
            if ticker not in stock_history:
                stock_history[ticker] = []
            stock_history[ticker].append((date, close_price))
    processed_records = []
    for ticker, history in stock_history.items():
        history.sort(key = lambda x: x[0])
        for i in range(1, len(history)):
            prev_date, prev_close = history[i - 1]
            curr_date, curr_close = history[i]
            if prev_close > 0:
                daily_return = (curr_close - prev_close) / prev_close * 100
                record = {
                    "ticker": ticker,
                    "date": curr_date,
                    "close": curr_close,
                    "daily_return": round(daily_return, 3),
                    "absolute_movement": round(abs(daily_return), 3),
                }
                processed_records.append(record)
    return processed_records

def heap_sort():
    pass

def merge_sort():
    pass