import numpy as np


def increasing_depths(
    raw_data_file: str = "./depths_rd.txt", window_size: int = 1
) -> int:
    """
    Calculates the number of times the provided depth measurements increases;
    `window_size` provides length of window for windowed sum of elements in
    `raw_data_file`
    """
    data = np.loadtxt(raw_data_file)
    positive_diffs = np.diff(
        np.convolve(data, np.ones(window_size, dtype=int), "valid")
    )
    return np.sum(positive_diffs > 0, axis=0)


if __name__ == "__main__":
    print(increasing_depths())  # Part 1 Solution: 1581
    print(increasing_depths(window_size=3))  # Part 2 Solution:
