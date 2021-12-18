import numpy as np
from skimage.morphology import local_minima


def read_data(raw_data_file: str) -> np.array:
    data = []
    with open(raw_data_file, 'r') as f:
        while (line := f.readline().rstrip()):
            data.append(list(line))
    return np.array(data).astype(int)


def find_sum_of_risk_levels(data: np.array) -> np.array:
    is_minima = local_minima(data, connectivity=1)
    return np.sum(data[is_minima] + 1)


if __name__ == "__main__":
    data = read_data('./vents.txt')
    print(find_sum_of_risk_levels(data))  # Part 1 Solution: 496
