from collections import Counter
from typing import List


def read_data(raw_data_file: str) -> List[int]:
    """
    Reads data from `raw_data_file` into a list of integers (`data`)
    """
    with open(raw_data_file, "r") as f:
        data = list(map(int, f.read().split(",")))
    return data


def fish_count_after_n_days(n: int, data: List[int]) -> int:
    """
    Returns the number of fish in the school of lanternfish after `n` days
    """
    # Initial state
    school_list = [0] * 9
    for timer, num_fish in Counter(data).items():
        school_list[timer] += num_fish

    # Update step
    for i in range(n):
        school_list[(i + 7) % 9] += school_list[i % 9]

    return sum(school_list)


if __name__ == "__main__":
    data = read_data("./lanternfish_rd.txt")
    print(fish_count_after_n_days(80, data))  # Part 1 Solution: 352872
    print(fish_count_after_n_days(256, data))  # Part 2 Solution: 1604361182149
