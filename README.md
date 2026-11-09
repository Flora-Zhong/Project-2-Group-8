# Top-K Stock Market Analysis System

## Project Description
This project is a Python-based application which effectively identify the Top-K largest daily stock movements, including gains, losses, and absolute movement, from a historical stock market dataset. To analyze and compare algorithm performance, this project implements Heap Sort and Merge Sort from scratch, and both of the two sorts will provide the Top K records after sorting. The time is provided for comparing these two sorts.

## Features
- Load and process a historical stock data from a CSV file.
- Calculate daily percentage returns and absolute movement for individual stocks in the dataset.
- Find the Top K largest daily gains, losses, or absolute price movements.
- Allow users to select the value of K and choose between Heap Sort, Merge Sort, or compare both by inputs.
- Display the selected stocks, dates, and percentage changes.
- Compare the execution time and verify if the two sorts return the same results when selecting the compare option.

## Algorithms Implemented From Scratch
- **Heap Sort**
  - An inplace sorting algorithm.
  - Build a max heap based on the selected mode.
  - Time Complexity: O(n log n).
  - Space Complexity for heap sort solely: O(log n).
  - Space Complexity for the entire function O(n).
- **Merge Sort**
  - A divide-and-conquer sorting algorithm.
  - Recursively divides the data and merge them.
  - Time Complexity: O(n log n).
  - Space Complexity: O(n).

## Dataset
The dataset needed for this project is `all_stocks_5yr.csv`, which is originated from Kaggle "S&P 500 stock data", and this CSV file is already included in this repository.

## Notes for Running the Code
- Our code is written with Python 3.12, so a Python 3.12 or higher version is recommended when running the code.
- Please run the `main.py` when running the code, and please do not run `algorithms.py`.
