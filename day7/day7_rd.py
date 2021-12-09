import numpy as np


def read_data(raw_data_file: str) -> np.array:
    """
    Reads data from `raw_data_file` into a list of integers (`data`)
    """
    with open(raw_data_file, "r") as f:
        data = np.array(list(map(int, f.read().split(","))))
    return data


def fuel_consumption(data: np.array) -> int:
    """
    Calculates the minimum amount of fuel expended by crab submarines to get
    horizontal alignment based on initial horizontal positions provided by `data`
    """
    x_med = np.median(data)
    return int(np.abs(data - x_med).sum())


if __name__ == "__main__":
    data = read_data("./crabs_rd.txt")
    print(fuel_consumption(data))  # Part 1 Solution: 342730
