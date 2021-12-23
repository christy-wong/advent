import re
from typing import List, Tuple

import numpy as np


def read_data(raw_data_file: str) -> Tuple[np.array, List[Tuple[str, int]]]:
    with open(raw_data_file, "r") as f:
        raw_coordinates, raw_instructions = f.read().split("\n\n")

    coordinates = [
        tuple(map(int, raw_coords.split(",")))
        for raw_coords in raw_coordinates.rstrip().split()
    ]
    max_x, max_y = tuple(map(lambda v: max(v), zip(*coordinates)))

    # Construct np.array of 0s (.)s and 1s (#)s
    data = np.zeros((max_x + 1, max_y + 1))
    zipped_coordinates = np.array(list(zip(*coordinates)))
    data[zipped_coordinates[0, :], zipped_coordinates[1, :]] = 1

    instructions = list(
        map(
            lambda x: (x[0], int(x[1])),
            [
                re.findall(r"[x,y]=\d+$", instruction)[0].split("=")
                for instruction in raw_instructions.split("\n")
            ],
        )
    )

    return data, instructions


if __name__ == "__main__":
    data, fold_instructions = read_data("./dots_rd.txt")
