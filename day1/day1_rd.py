import numpy as np


def main():
    """
    Calculates the number of times the provided depth measurements increases
    """
    data = np.loadtxt('./depths_rd.txt')
    positive_diffs = np.sum(np.diff(data) > 0, axis=0)
    return positive_diffs


if __name__ == "__main__":
    print(main())  # Solution: 1581
