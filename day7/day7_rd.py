import numpy as np
from scipy.optimize import minimize_scalar


def read_data(raw_data_file: str) -> np.array:
    """
    Reads data from `raw_data_file` into a list of integers (`data`)
    """
    with open(raw_data_file, "r") as f:
        data = np.array(list(map(int, f.read().split(","))))
    return data


def linear_scale_cost_function(data: np.array, m: np.array) -> int:
    """
    Cost function for when the fuel costs incrementally scale linearly with steps taken
    """
    d = np.abs(data.astype(int) - m.astype(int))
    return ((d ** 2 + d) / 2).sum().astype(int)


def fuel_consumption(data: np.array, cost_scale="constant") -> int:
    """
    Calculates the minimum amount of fuel expended by crab submarines to get
    horizontal alignment based on initial horizontal positions provided by `data`
    """
    d = np.abs(data - np.median(data))
    l1_cost_min = int(d.sum())

    # Choose interval of integer points around the mean
    m_star = np.mean(data)
    search_interval = data.max() - data.min() / 4
    m_low, m_high = m_star - search_interval, m_star + search_interval

    align_pos = minimize_scalar(
        linear_scale_cost_function, (m_low, m_high), args=(data,)
    )
    m = int(align_pos["x"])

    if cost_scale == "constant":
        return l1_cost_min
    elif cost_scale == "linear":
        return int(linear_scale_cost_function(data, np.ones_like(data) * m))


if __name__ == "__main__":
    data = read_data("./crabs_rd.txt")
    test_data = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])

    print(fuel_consumption(data))  # Part 1 Solution: 342730
    print(fuel_consumption(data, cost_scale="linear"))  # Part 2 Solution: 92335207
    print(linear_scale_cost_function(data, np.mean(data)))  # 92335207
    # Notice that the mean works for my given input data, though some searching
    # (above or below the float value) for integers that work may be required.
    # See TEST section below.

    # TEST
    print(fuel_consumption(test_data))  # Test 1 Solution: 37 is correct
    print(fuel_consumption(test_data, cost_scale="linear"))  # Test 2 Solution: 168
    print(linear_scale_cost_function(test_data, np.mean(test_data)))  # 170
