from collections import Counter
from itertools import tee
from typing import Dict, List, Tuple


def read_data(raw_data_file: str) -> Tuple[str, Dict[str, str]]:
    """
    Reads the `polymer_template` and pair insertion rules into a string and
    dict, respectively
    """
    pair_insertion_map = {}
    with open(raw_data_file, "r") as f:
        polymer_template = f.readline().rstrip()
        f.readline()  # Skip line
        while line := f.readline().rstrip():
            pair_insertion_map[line[:2]] = line[-1]
    return polymer_template, pair_insertion_map


def pairwise(string: str) -> List[str]:
    """
    Returns list of all adjacent pairs of characters in `string` in order
    """
    a, b = tee(string)
    next(b, None)
    return ["".join(pair) for pair in zip(a, b)]


def pair_insertion_n_times(
    polymer_template: str, pair_insertion_map: Dict[str, str], n: int
) -> str:
    for _ in range(n):
        new_polymer = ""
        for pair in pairwise(polymer_template):
            new_polymer += pair[0] + pair_insertion_map[pair]
        polymer_template = new_polymer + polymer_template[-1]
    return polymer_template


def range_of_element_frequencies(polymer_template: str) -> int:
    counter = Counter(polymer_template)
    return counter.most_common()[0][1] - counter.most_common()[-1][1]


if __name__ == "__main__":
    polymer_template, pair_insertion_map = read_data("./polymers_rd.txt")
    print(polymer_template)
    print(
        range_of_element_frequencies(
            pair_insertion_n_times(polymer_template, pair_insertion_map, 10)
        )
    )  # Part 1 Solution: 2975
