from typing import List

import numpy as np
from skimage.morphology import flood, local_minima


def read_data(raw_data_file: str) -> np.array:
    data = []
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            data.append(list(line))
    return np.array(data).astype(int)


def find_sum_of_risk_levels(data: np.array) -> np.array:
    """
    Finds the low points in the 2D-array of integers, `data`; adds 1 to these low
    points and sums them all
    """
    is_minima = local_minima(data, connectivity=1)
    return np.sum(data[is_minima] + 1)


def get_basin_size(data: np.array, i: int, j: int) -> int:
    """
    Finds the size of the basin containing low point at position `i`, `j` in
    `data`
    """
    tolerance = 9 - 1 - data[i, j]
    return np.sum(flood(data, (i, j), connectivity=1, tolerance=tolerance))


def get_three_largest_basins(data: np.array) -> List[int]:
    """
    Finds the three largest basins in 2D-array of integers, `data`
    """
    largest_basin_sizes = [0, 0, 0]
    low_point_indices = zip(*np.where(local_minima(data, connectivity=1)))
    for i, j in low_point_indices:
        basin_size = get_basin_size(data, i, j)
        smalled_basin_size_saved = min(largest_basin_sizes)
        if basin_size > smalled_basin_size_saved:
            largest_basin_sizes.remove(smalled_basin_size_saved)
            largest_basin_sizes.append(basin_size)
    return largest_basin_sizes


def find_product_of_three_largest_basins(data: np.array) -> int:
    """
    Multiples the size of the three largest basins together
    """
    return np.product(get_three_largest_basins(data))


if __name__ == "__main__":
    data = read_data("./vents.txt")
    print(find_sum_of_risk_levels(data))  # Part 1 Solution: 496
    print(find_product_of_three_largest_basins(data))  # Part 2 Solution: 902880
