from collections import Counter
from collections.abc import Iterable
from itertools import chain
from typing import List, Tuple

SEGMENT_COUNT_TO_NUMBER_MAP = {
    2: 1,
    3: 7,
    4: 4,
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: 8,
}


def read_data(raw_data_file: str) -> List[Tuple[List[str]]]:
    """
    Reads the unique signal patterns and output values into two lists
    """
    data = []
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            split_data = line.split("|")
            data.append(tuple(part.split() for part in split_data))
    return data


def decode_display(
    unique_signal_patterns: List[str], output_values: List[str]
) -> List[int]:
    """
    Constructs dictionary to decode scrambled signal patterns (each
    `unique_signal_pattern` is associated with its corresponding digit)
    """
    unique_signal_pattern_map = {}
    for signal_pattern in unique_signal_patterns:
        unique_signal_pattern_map[
            "".join(sorted(signal_pattern))
        ] = SEGMENT_COUNT_TO_NUMBER_MAP[len(signal_pattern)]
    number_to_signal_pattern_map = {
        number: signal_pattern
        for signal_pattern, number in unique_signal_pattern_map.items()
        if not isinstance(number, Iterable)
    }
    length_sorted_unique_signal_pattern_map = dict(
        sorted(unique_signal_pattern_map.items(), key=lambda x: len(x[0]), reverse=True)
    )
    while non_deterministic_numbers := any(
        map(lambda x: isinstance(x, Iterable), unique_signal_pattern_map.values())
    ):
        for (
            signal_pattern,
            possible_values,
        ) in length_sorted_unique_signal_pattern_map.items():
            if isinstance(possible_values, Iterable):
                if len(signal_pattern) == 6:
                    if set(signal_pattern) > set(number_to_signal_pattern_map[4]):
                        identified_number = 9
                    elif set(signal_pattern) > set(number_to_signal_pattern_map[1]):
                        identified_number = 0
                    else:
                        identified_number = 6
                if len(signal_pattern) == 5:
                    if set(signal_pattern) > set(number_to_signal_pattern_map[7]):
                        identified_number = 3
                    elif set(signal_pattern) < set(number_to_signal_pattern_map[6]):
                        identified_number = 5
                    else:
                        identified_number = 2
                unique_signal_pattern_map[signal_pattern] = identified_number
                number_to_signal_pattern_map[identified_number] = signal_pattern

    # Decode display
    return [
        unique_signal_pattern_map["".join(sorted(digit))] for digit in output_values
    ]


def count_easily_decoded_numbers(data: List[Tuple[List[str]]]) -> int:
    """
    Counts the number of occurrences of 1, 4, 7, 8 output values
    """
    counter = Counter(list(chain.from_iterable([decode_display(*row) for row in data])))
    freq = 0
    for i in (1, 4, 7, 8):
        freq += counter[i]
    return freq


def sum_all_decoded_output_values(data: List[Tuple[List[str]]]) -> int:
    """
    Returns the sum of all of the decoded digits (output values)
    """
    decoded_output_values = [decode_display(*row) for row in data]
    return sum(sum(j * 10**i for i, j in enumerate(reversed(row))) for row in decoded_output_values)


if __name__ == "__main__":
    data = read_data("./notes_rd.txt")
    print(count_easily_decoded_numbers(data))  # Part 1 Solution: 452
    print(sum_all_decoded_output_values(data))  # Part 1 Solution: 1096964
