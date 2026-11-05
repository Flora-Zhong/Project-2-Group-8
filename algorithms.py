import csv

def data_processing(filepath: str) -> list[dict]:
    """
    Read a historical stock data CSV file, calculate daily returns and absolute movements,
    and returns processed records.

    Parameters:
        filepath (string): The path to the input CSV file.

    Returns:
        A list of dictionaries containing ticker, date, close, daily_return, and absolute_movement.
    """
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
        # Sort by date to make ensure correct return calculation.
        history.sort(key = lambda x: x[0])
        for i in range(1, len(history)):
            prev_date, prev_close = history[i - 1]
            curr_date, curr_close = history[i]
            if prev_close > 0: # Prevent division by 0.
                daily_return = (curr_close - prev_close) / prev_close * 100
                record = {
                    "ticker": ticker,
                    "date": curr_date,
                    "close": curr_close,
                    "daily_return": daily_return,
                    "absolute_movement": abs(daily_return)
                }
                processed_records.append(record)
    return processed_records

def heap_sort_compare(a: dict, b: dict, mode: str) -> bool:
    """
    Compare two stock records and see if record a has a higher priority than record b.

    Parameters:
        a (dict): The first stock record.
        b (dict): The second stock record.
        mode (string): The mode ("gains", "losses", or "absolute") to compare records.

    Returns:
        A boolean value indicating if record a has a higher priority than record b.
    """
    # Compare main metric based on different modes.
    if mode == "gains":
        if a["daily_return"] != b["daily_return"]:
            return a["daily_return"] > b["daily_return"]
    elif mode == "losses":
        if a["daily_return"] != b["daily_return"]:
            return a["daily_return"] < b["daily_return"]
    elif mode == "absolute":
        if a["absolute_movement"] != b["absolute_movement"]:
            return a["absolute_movement"] > b["absolute_movement"]
    # Compare ticker when the daily return or absolute movement is equal.
    if a["ticker"] != b["ticker"]:
        return a["ticker"] < b["ticker"]
    # Compare date when ticker is also equal.
    return a["date"] < b["date"]

def heap_sort_sift_down(arr: list[dict], n: int, i: int, mode: str) -> None:
    """
    Recursively sift down the element at index i to maintain a max-heap.

    Parameters:
        arr (list[dict]): The list of stock records.
        n (int): The size of the heap.
        i (int): The index of the current node.
        mode (string): The mode ("gains", "losses", or "absolute") to compare records.

    Returns:
        None.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    # Check if left child exist and is larger than the current largest.
    if (left < n) and (heap_sort_compare(arr[left], arr[largest], mode)):
        largest = left
    # Check if right child exist and is larger than the current largest.
    if (right < n) and (heap_sort_compare(arr[right], arr[largest], mode)):
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heap_sort_sift_down(arr, n, largest, mode)

def heap_sort(arr: list[dict], mode: str) -> None:
    """
    Perform heap sort on the stock records.

    Parameters:
        arr (list[dict]): The list of stock records.
        mode (string): The mode ("gains", "losses", or "absolute") to compare records.

    Returns:
        None.
    """
    n = len(arr)
    # Build max-heap.
    for i in range(n // 2 - 1, -1, -1):
        heap_sort_sift_down(arr, n, i, mode)
    # Extract each element from the heap and swap.
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heap_sort_sift_down(arr, i, 0, mode)

def top_k_heap_sort(records: list[dict], k: int, mode: str = "absolute") -> list[dict]:
    """
    Find the top k records using heap sort.

    Parameters:
        records (list[dict]): The list of processed stock records.
        k (int): The number of top records to return.
        mode (string): The mode ("gains", "losses", or "absolute") to compare records.

    Returns:
        A list of dictionaries containing top k records.
    """
    # Checking if k is valid or not.
    if not isinstance(k, int):
        raise TypeError("k must be an integer.")
    elif k < 0:
        raise ValueError("k must be greater than or equal to 0.")
    elif k == 0:
        return []
    # Checking if mode is valid or not.
    if mode not in ["gains", "losses", "absolute"]:
        raise ValueError("mode must be 'gains', 'losses' or 'absolute'.")
    # Filter records based on mode.
    filter_records = []
    for record in records:
        if (mode == "gains") and (record["daily_return"] > 0):
            filter_records.append(record)
        elif (mode == "losses") and (record["daily_return"] < 0):
            filter_records.append(record)
        elif (mode == "absolute") and ("absolute_movement" in record):
            filter_records.append(record)
    actual_k = min(k, len(filter_records))
    if actual_k == 0:
        return []
    data = filter_records.copy() # Avoid changing the original data.
    heap_sort(data, mode)
    # Take the last k values and reverse since it is in ascending order.
    top_k_results = data[-actual_k:][::-1]
    return top_k_results

def merge_sort():
    pass