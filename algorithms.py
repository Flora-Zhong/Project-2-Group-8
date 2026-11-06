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

'''Merge sort starts'''

def _validate_merge_sort_arguments(k: int, mode: str) -> None:
    """Validate the public Top-K merge sort arguments."""
    if mode not in ["gains", "losses", "absolute"]:
        raise ValueError("mode must be 'gains', 'losses' or 'absolute'.")
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer, not a boolean.")
    if k < 0:
        raise ValueError("k must be greater than or equal to 0.")


def _merge_sort_is_eligible(record: dict, mode: str) -> bool:
    """Return whether a record belongs in the requested result category."""
    if mode == "gains":
        return record["daily_return"] > 0
    if mode == "losses":
        return record["daily_return"] < 0
    return "absolute_movement" in record


def is_better(record_a: dict, record_b: dict, mode: str) -> bool:
    """Return whether record_a belongs before record_b in the final ranking.

    Ties are resolved by ticker alphabetically and then by the earlier date.
    If all ranking keys match, False is returned so merge sort keeps the
    original order of otherwise identical records.
    """
    if mode == "gains":
        if record_a["daily_return"] != record_b["daily_return"]:
            return record_a["daily_return"] > record_b["daily_return"]
    elif mode == "losses":
        if record_a["daily_return"] != record_b["daily_return"]:
            return record_a["daily_return"] < record_b["daily_return"]
    elif mode == "absolute":
        if record_a["absolute_movement"] != record_b["absolute_movement"]:
            return record_a["absolute_movement"] > record_b["absolute_movement"]
    else:
        raise ValueError("mode must be 'gains', 'losses' or 'absolute'.")

    ticker_a = record_a["ticker"].upper()
    ticker_b = record_b["ticker"].upper()
    if ticker_a != ticker_b:
        return ticker_a < ticker_b
    return record_a["date"] < record_b["date"]


def _merge(left: list[dict], right: list[dict], mode: str) -> list[dict]:
    """Merge two ranked lists into one ranked list."""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if is_better(right[right_index], left[left_index], mode):
            merged.append(right[right_index])
            right_index += 1
        else:
            # Keep the left record first when all ranking keys are equal.
            merged.append(left[left_index])
            left_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def _merge_sort_records(records: list[dict], mode: str) -> list[dict]:
    """Recursively rank already-filtered records using merge sort."""
    if len(records) <= 1:
        return list(records)

    midpoint = len(records) // 2
    left_sorted = _merge_sort_records(records[:midpoint], mode)
    right_sorted = _merge_sort_records(records[midpoint:], mode)
    return _merge(left_sorted, right_sorted, mode)


def merge_sort(records: list[dict], mode: str = "absolute") -> list[dict]:
    """Return eligible stock records ranked best to worst with merge sort.
    """
    if mode not in ["gains", "losses", "absolute"]:
        raise ValueError("mode must be 'gains', 'losses' or 'absolute'.")

    eligible_records = [
        record for record in records if _merge_sort_is_eligible(record, mode)
    ]
    return _merge_sort_records(eligible_records, mode)


def top_k_merge_sort(
    records: list[dict], k: int, mode: str = "absolute"
) -> list[dict]:
    """Return up to k records, best to worst, using merge sort from scratch."""
    _validate_merge_sort_arguments(k, mode)
    if k == 0:
        return []

    ranked_records = merge_sort(records, mode)
    return ranked_records[:k]
