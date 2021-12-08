from collections import Counter
from typing import List


def read_diagnostic_report(raw_data_file: str) -> List[List[int]]:
    """
    Reads raw data into a list of lists of bits
    """
    with open(raw_data_file, "r") as f:
        data = []
        while line := f.readline().rstrip():
            data.append(list(map(int, line)))
    return data


def convert_bit_list_to_int(bit_list: List[int]) -> int:
    """
    Converts a list of bits (e.g., [1, 0, 0, 1, 1]) to its integer form
    """
    return sum(j << i for i, j in enumerate(reversed(bit_list)))


def common_bits(commonality: str, data: List[List[int]]) -> List[int]:
    """
    Returns list of bits based on `commonality` specified for each index
    position in `data`
    """
    common_bits = []
    for col in list(zip(*data)):
        freq_dict = Counter(col)
        if commonality == "most":
            common_bit = (
                max(freq_dict, key=freq_dict.get)
                if not freq_dict[0] == freq_dict[1]
                else 1
            )
        elif commonality == "least":
            common_bit = (
                min(freq_dict, key=freq_dict.get)
                if not freq_dict[0] == freq_dict[1]
                else 0
            )
        else:
            raise ValueError("Invalid bit criteria")
        common_bits.append(common_bit)
    return common_bits


def matches_bit_at_index(row: List[int], bit: int, pos: int) -> bool:
    """
    Determines whether the bit at `pos` in `row` matches the passed in `bit`
    """
    return row[pos] == bit


def power_consumption(data: List[List[int]]) -> int:
    """
    Produces decimal representation of the product of two binary integers
    where the first is the `gamma_rate` and the second is the `epsilon_rate`
    """
    if not all(len(data[0]) == len(row) for row in data):
        raise ValueError("Inconsistent bit lengths in input data")
    bits = len(data[0])
    gamma_rate = convert_bit_list_to_int(common_bits("most", data))
    epsilon_rate = gamma_rate ^ int("1" * bits, 2)
    return gamma_rate * epsilon_rate


def filter_data_on_bit_criteria_matching(
    data: List[List[int]], commonality, pos=0
) -> List[List[int]]:
    """
    Recursively filters the `data` down to the `row` that matches the most `common_bits`
    from left to right
    """
    if len(data) == 1 or all(data[0] == row for row in data):
        return data
    else:
        data = list(
            filter(
                lambda row: matches_bit_at_index(
                    row, bit=common_bits(commonality, data)[pos], pos=pos
                ),
                data,
            )
        )
        pos += 1
        return filter_data_on_bit_criteria_matching(data, commonality, pos)


def life_support_rating(data: List[List[int]]) -> int:
    """
    Produces decimal representation of the product of two binary integers
    where the first is the `oxygen_generator_rating` and the second is the
    `co2_scrubber_rating`
    """
    oxygen_generator_rating = convert_bit_list_to_int(
        filter_data_on_bit_criteria_matching(data, commonality="most")[0]
    )
    co2_scrubber_rating = convert_bit_list_to_int(
        filter_data_on_bit_criteria_matching(data, commonality="least")[0]
    )
    return oxygen_generator_rating * co2_scrubber_rating


if __name__ == "__main__":
    data = read_diagnostic_report("./rays_rd.txt")
    print(power_consumption(data))  # Part 1 Solution: 3277364
    print(life_support_rating(data))  # Part 2 Solution: 5736383
