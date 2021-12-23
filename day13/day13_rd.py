import re
from typing import List, Tuple

import numpy as np


def read_data(raw_data_file: str) -> Tuple[np.array, List[Tuple[str, int]]]:
    """
    Returns `data` represented as 2D-array and `fold_instructions` as list of
    tuples where each tuple contains the direction of the fold and index on
    which to fold
    """
    with open(raw_data_file, "r") as f:
        raw_coordinates, raw_instructions = f.read().split("\n\n")

    coordinates = [
        tuple(map(int, raw_coords.split(",")))
        for raw_coords in raw_coordinates.rstrip().split()
    ]
    # Switch orientation to match problem
    cols_len, rows_len = tuple(map(lambda v: max(v) + 1, zip(*coordinates)))

    # Construct np.array of 0s (.)s and 1s (#)s
    data = np.zeros((rows_len, cols_len))
    zipped_coordinates = np.array(list(zip(*coordinates)))
    data[zipped_coordinates[1, :], zipped_coordinates[0, :]] = 1

    fold_instructions = list(
        map(
            lambda x: (x[0], int(x[1])),
            [
                re.findall(r"[x,y]=\d+$", instruction)[0].split("=")
                for instruction in raw_instructions.split("\n")
            ],
        )
    )

    return data.astype(int), fold_instructions


def fold_result(data: np.array, fold_instruction: Tuple[str, int]) -> np.array:
    """
    Folds the `data` input according to `fold_instruction` and returns the
    resultant array where positive integer elements are reduced to 1s and zeros
    remain zeros
    """
    if fold_instruction[0] == "y":
        top, bottom = (
            data[: fold_instruction[1], :],
            np.flipud(data[(fold_instruction[1] + 1) :, :]),
        )
        if (pad_len := top.shape[0] - bottom.shape[0]) > 0:
            bottom = np.pad(bottom, ((abs(pad_len), 0), (0, 0)), "constant")
        else:
            top = np.pad(top, ((abs(pad_len), 0), (0, 0)), "constant")
        result = top + bottom
    elif fold_instruction[0] == "x":
        left, right = (
            data[:, : fold_instruction[1]],
            np.fliplr(data[:, (fold_instruction[1] + 1) :]),
        )
        if (pad_len := left.shape[1] - right.shape[1]) > 0:
            right = np.pad(right, ((0, 0), (abs(pad_len), 0)), "constant")
        else:
            left = np.pad(left, ((0, 0), (abs(pad_len), 0)), "constant")
        result = right + left
    else:
        raise ValueError("Invalid `fold_instruction` direction")
    return (result > 0).astype(int)


def complete_folds(
    data: np.array, fold_instructions: List[Tuple[str, int]]
) -> np.array:
    """
    Returns final array after all `fold_instructions` are applied to original
    `data` input
    """
    for fold_instruction in fold_instructions:
        data = fold_result(data, fold_instruction)
    pattern = "\n".join(
        ["".join(map(lambda k: "#" if k == 1 else ".", line)) for line in data.tolist()]
    )
    print(pattern)


if __name__ == "__main__":
    data, fold_instructions = read_data("./dots_rd.txt")
    print(fold_result(data, fold_instructions[0]).sum())  # Part 1 Solution: 842
    complete_folds(data, fold_instructions)  # Part 2 Solution: BFKRCJZU

    #   ###..####.#..#.###...##....##.####.#..#.
    #   #..#.#....#.#..#..#.#..#....#....#.#..#.
    #   ###..###..##...#..#.#.......#...#..#..#.
    #   #..#.#....#.#..###..#.......#..#...#..#.
    #   #..#.#....#.#..#.#..#..#.#..#.#....#..#.
    #   ###..#....#..#.#..#..##...##..####..##..
