import numpy as np


def read_data(raw_data_file: str) -> np.array:
    data = []
    with open(raw_data_file, 'r') as f:
        while (line := f.readline().rstrip()):
            data.append(list(line))
    return np.array(data).astype(int)


if __name__ == "__main__":
    data = read_data('./vents.txt')
    print(data)
