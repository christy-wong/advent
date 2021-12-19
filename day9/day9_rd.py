from typing import List, Tuple

import numpy as np
from skimage.morphology import local_minima


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


def is_inside_basin(data: np.array, i: int, j: int, basin_points: List[Tuple]) -> bool:
    """
    Returns boolean for whether `i`, `j` is unfilled yet if inside basin or
    """
    try:
        if (data[i, j] == 9) or ((i, j) in basin_points) or (i < 0) or (j < 0):
            return False
    except IndexError:
        return False

    return True


def recursive_flood(data: np.array, i: int, j: int, basin_points: List[Tuple]) -> int:
    """
    Finds the indices comprising the basin containing low point at position `i`, `j` in
    `data` recursively
    """
    if not is_inside_basin(data, i, j, basin_points):
        return

    basin_points.append((i, j))

    recursive_flood(data, i + 1, j, basin_points)
    recursive_flood(data, i - 1, j, basin_points)
    recursive_flood(data, i, j + 1, basin_points)
    recursive_flood(data, i, j - 1, basin_points)


def get_three_largest_basins(data: np.array) -> List[int]:
    """
    Finds the three largest basins in 2D-array of integers, `data`
    """
    largest_basin_sizes = [0, 0, 0]
    low_point_indices = zip(*np.where(local_minima(data, connectivity=1)))
    for i, j in low_point_indices:
        basin_points = []
        recursive_flood(data, i, j, basin_points)
        basin_size = len(basin_points)
        smalled_basin_size_saved = min(largest_basin_sizes)
        if basin_size > smalled_basin_size_saved:
            largest_basin_sizes.remove(smalled_basin_size_saved)
            largest_basin_sizes.append(basin_size)
    return largest_basin_sizes


def find_product_of_three_largest_basins(data: np.array) -> int:
    """
    Multiplies the size of the three largest basins together
    """
    return np.product(get_three_largest_basins(data))


if __name__ == "__main__":
    data = read_data("./vents_rd.txt")
    print(find_sum_of_risk_levels(data))  # Part 1 Solution: 496
    print(find_product_of_three_largest_basins(data))  # Part 2 Solution: 902880
