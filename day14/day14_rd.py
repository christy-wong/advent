from collections import Counter
from functools import lru_cache
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


def count_element_frequencies_n_times(
    polymer_template: str, pair_insertion_map: Dict[str, str], n: int
):
    """
    Returns Counter object counting frequencies of letters after `n` insertion
    steps on original `polymer_template`
    """

    @lru_cache(maxsize=None)
    def recursive_pair_insertion_n_times(
        polymer_pair: str,
        n: int,
    ) -> Counter:
        """
        Recursively counts the frequency of letters added over `n` steps starting
        with a `polymer_pair`
        """
        counter = Counter()

        # Base case
        if n == 0:
            return counter

        # Add new letter to counter
        new_letter = pair_insertion_map[polymer_pair]
        counter.update(new_letter)
        new_polymer_trio = polymer_pair[0] + new_letter + polymer_pair[-1]

        # Recursive case for resultant two, new pairs in `new_polymer_trio`
        for new_polymer_pair in pairwise(new_polymer_trio):
            counter.update(recursive_pair_insertion_n_times(new_polymer_pair, n - 1))
        return counter

    master_counter = Counter(polymer_template)
    for polymer_pair in pairwise(polymer_template):
        master_counter.update(recursive_pair_insertion_n_times(polymer_pair, n))
    return master_counter


def range_of_element_frequencies(counter: Counter) -> int:
    """
    Returns difference between frequency of most and least common items in
    `counter` Counter object
    """
    return counter.most_common()[0][1] - counter.most_common()[-1][1]


if __name__ == "__main__":
    polymer_template, pair_insertion_map = read_data("./polymers_rd.txt")
    print(
        range_of_element_frequencies(
            count_element_frequencies_n_times(polymer_template, pair_insertion_map, 10)
        )
    )  # Part 1 Solution: 2975
    print(
        range_of_element_frequencies(
            count_element_frequencies_n_times(polymer_template, pair_insertion_map, 40)
        )
    )  # Part 2 Solution: 3015383850689
