from typing import Set, Tuple

import numpy as np
from scipy.ndimage import convolve

KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def read_data(raw_data_file: str) -> np.array:
    """
    Reads octopuses' energy levels into 2D-array of integers
    """
    with open(raw_data_file, "r") as f:
        data = [[int(n) for n in line.rstrip()] for line in f.readlines()]
    return np.array(data)


def find_flashes_indices(data: np.array) -> Set[Tuple[int]]:
    """
    Returns the set of `i`, `j` coordinates of octopuses that flashed in a given
    state of `data`
    """
    return {(i, j) for i, j in np.argwhere(data > 9)}


def increment_neighbors_of_flashes(data: np.array) -> np.array:
    """
    Returns array with all neighboring octopuses' energy incremented +1 for all
    octopuses in `data` with energy level > 9
    """
    data += convolve(
        (data > 9).astype(int),
        KERNEL,  # No need to np.flip because `KERNEL` is rotationally symmetric
        mode="constant",
    )
    return data


def take_step(data: np.array) -> np.array:
    """
    Returns octopuses energy states after one step
    """
    next_state = data + 1
    recent_flash_idx = find_flashes_indices(next_state)
    all_flash_idx = set()
    while unaccounted_flash_idx := recent_flash_idx - all_flash_idx:
        next_state = increment_neighbors_of_flashes(next_state)
        all_flash_idx |= unaccounted_flash_idx
        next_state[tuple(zip(*all_flash_idx))] = 0
        recent_flash_idx = find_flashes_indices(next_state)
    return next_state


def flashes_after_n_steps(data: np.array, n: int) -> int:
    """
    Counts the number of total flashes given an initial state of octopuses'
    energy levels in `data`
    """
    flashes = 0
    for _ in range(n):
        data = take_step(data)
        flashes += data.size - np.count_nonzero(data)
    return flashes


if __name__ == "__main__":
    data = read_data("./octopuses_rd.txt")
    print(flashes_after_n_steps(data, 100))  # Part 1 Solution: 1594
