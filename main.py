import algorithms
from pathlib import Path
from time import perf_counter


DEFAULT_DATA_FILE = Path(__file__).with_name("all_stocks_5yr.csv")


def print_menu() -> None:
    """Print the main menu for the Top-K Stock Market Analysis System."""
    print("\n" + "=" * 62)
    print("TOP-K STOCK MARKET ANALYSIS SYSTEM")
    print("=" * 62)
    print("1. Load stock market dataset")
    print("2. Find Top K largest daily gains")
    print("3. Find Top K largest daily losses")
    print("4. Find Top K largest absolute movements")
    print("5. Compare Heap Sort and Merge Sort")
    print("0. Exit")


def read_nonnegative_k() -> int:
    """Prompt until the user provides a nonnegative integer K."""
    while True:
        raw_k = input("Enter K (number of results): ").strip()
        try:
            k = int(raw_k)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if k < 0:
            print("K must be greater than or equal to 0.")
            continue
        return k


def read_mode() -> str:
    """Prompt the user to select gains, losses, or absolute movement."""
    choices = {"1": "gains", "2": "losses", "3": "absolute"}
    while True:
        print("\nChoose a result type:")
        print("1. Largest daily gains")
        print("2. Largest daily losses")
        print("3. Largest absolute movements")
        selection = input("Selection: ").strip()
        if selection in choices:
            return choices[selection]
        print("Please choose 1, 2, or 3.")


def read_algorithm_choice() -> str:
    """Prompt the user to select an algorithm or run both for comparison."""
    while True:
        print("\nChoose an algorithm:")
        print("1. Heap Sort")
        print("2. Merge Sort")
        print("3. Compare both")
        selection = input("Selection: ").strip()
        if selection in {"1", "2", "3"}:
            return selection
        print("Please choose 1, 2, or 3.")


def format_results(results: list[dict], mode: str, algorithm_name: str) -> str:
    """Return ranked stock records as a readable console table."""
    title = f"TOP {len(results)} {mode.upper()} DAILY MOVEMENTS - {algorithm_name}"
    lines = ["\n" + title, "-" * len(title)]
    if not results:
        lines.append("No records matched the selected criteria.")
        return "\n".join(lines)

    lines.append(f"{'Rank':<6}{'Ticker':<10}{'Date':<14}{'Daily Return'}")
    for rank, record in enumerate(results, start=1):
        daily_return = record["daily_return"]
        lines.append(
            f"{rank:<6}{record['ticker']:<10}{record['date']:<14}"
            f"{daily_return:+.3f}%"
        )
    return "\n".join(lines)


def run_algorithm(records: list[dict], k: int, mode: str, algorithm_name: str):
    """Run one selected algorithm and return its results and elapsed milliseconds."""
    if algorithm_name == "Heap Sort":
        algorithm = algorithms.top_k_heap_sort
    else:
        algorithm = algorithms.top_k_merge_sort

    start_time = perf_counter()
    results = algorithm(records, k, mode)
    elapsed_ms = (perf_counter() - start_time) * 1000
    return results, elapsed_ms


def compare_algorithms(records: list[dict], k: int, mode: str) -> None:
    """Run both algorithms, display their common output, and report timings."""
    heap_results, heap_time = run_algorithm(records, k, mode, "Heap Sort")
    merge_results, merge_time = run_algorithm(records, k, mode, "Merge Sort")

    print(format_results(merge_results, mode, "Merge Sort"))
    print("\nALGORITHM PERFORMANCE COMPARISON")
    print("-" * 38)
    print(f"Heap Sort:  {heap_time:.3f} ms")
    print(f"Merge Sort: {merge_time:.3f} ms")
    if heap_results == merge_results:
        print("Verification: both algorithms returned the same ordered Top-K results.")
    else:
        print("Verification: results differ. Check the ranking and tie-breaking rules.")


def run_top_k_query(records: list[dict], mode: str) -> None:
    """Collect K and algorithm choice, then show the requested Top-K output."""
    k = read_nonnegative_k()
    algorithm_choice = read_algorithm_choice()

    if algorithm_choice == "3":
        compare_algorithms(records, k, mode)
        return

    algorithm_name = "Heap Sort" if algorithm_choice == "1" else "Merge Sort"
    results, elapsed_ms = run_algorithm(records, k, mode, algorithm_name)
    print(format_results(results, mode, algorithm_name))
    print(f"\nExecution time: {elapsed_ms:.3f} ms")


def load_dataset() -> list[dict] | None:
    """Load the repository CSV file and return processed stock records."""
    if not DEFAULT_DATA_FILE.is_file():
        print(f"Dataset not found: {DEFAULT_DATA_FILE}")
        return None

    print(f"\nLoading {DEFAULT_DATA_FILE.name}...")
    start_time = perf_counter()
    try:
        records = algorithms.data_processing(DEFAULT_DATA_FILE)
    except (OSError, KeyError, ValueError, TypeError) as error:
        print(f"Could not load the dataset: {error}")
        return None

    elapsed_seconds = perf_counter() - start_time
    print(f"Loaded {len(records):,} processed records in {elapsed_seconds:.3f} seconds.")
    return records


def main() -> None:
    """Run the interactive Top-K Stock Market Analysis console application."""
    records = None
    mode_by_choice = {"2": "gains", "3": "losses", "4": "absolute"}

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            return
        if choice == "1":
            records = load_dataset()
            continue
        if choice in mode_by_choice:
            if records is None:
                print("Please load the dataset first by selecting option 1.")
            else:
                run_top_k_query(records, mode_by_choice[choice])
            continue
        if choice == "5":
            if records is None:
                print("Please load the dataset first by selecting option 1.")
            else:
                mode = read_mode()
                k = read_nonnegative_k()
                compare_algorithms(records, k, mode)
            continue

        print("Please choose a menu option from 0 to 5.")

if __name__ == '__main__':
    main()
