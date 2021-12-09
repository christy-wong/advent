from collections import Counter
from itertools import chain
from typing import List, Tuple


def read_data(raw_data_file: str) -> List[List[Tuple[int]]]:
    """
    Read the pairs of points parameterizing the line segments of the vents
    """
    data = []
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            line_coordinates = []
            for raw_line_coordinate in line.split(" -> "):
                line_coordinates.append(tuple(map(int, raw_line_coordinate.split(","))))
            data.append(line_coordinates)
    return data


def is_horizontal_or_vertical_line_segment(line_coordinates: List[Tuple[int]]) -> bool:
    """
    Returns `True` if points bound a perfectly horizontal or vertical line segment
    """
    x1, y1, x2, y2 = *line_coordinates[0], *line_coordinates[1]
    return (x1 == x2) or (y1 == y2)


def draw_line_segment(points: List[Tuple[int]]) -> List[Tuple[int]]:
    """
    Enumerate integer-valued coordinate pairs comprising a line segment
    """
    p1, p2 = points
    if p1[0] == p2[0]:
        return [(p1[0], y) for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1)]
    elif p1[1] == p2[1]:
        return [(x, p1[1]) for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1)]
    elif abs(p1[0] - p2[0]) == abs(p1[1] - p2[1]):
        x_displacement = p2[0] - p1[0]
        y_displacement = p2[1] - p1[1]
        displacement_list = list(
            zip(
                range(
                    0,
                    x_displacement + x_displacement // abs(x_displacement),
                    x_displacement // abs(x_displacement),
                ),
                range(
                    0,
                    y_displacement + y_displacement // abs(y_displacement),
                    y_displacement // abs(y_displacement),
                ),
            )
        )
        return [
            (p1[0] + x_delta, p1[1] + y_delta)
            for x_delta, y_delta in displacement_list
        ]
    else:
        return []


def count_intersections(
    data: List[List[Tuple[int]]], only_horizontal_or_vertical_line_segments=True
) -> int:
    """
    Returns the number of intersections of the line segments parameterized by
    `data`; `only_horizontal_and_vertical_line_segments` filters `data` for perfectly
    horizontal or vertical line segments
    """
    if only_horizontal_or_vertical_line_segments:
        data = list(filter(is_horizontal_or_vertical_line_segment, data))
    covered_points = list(
        chain(*[draw_line_segment(point_pair) for point_pair in data])
    )
    return len([p for p, freq in Counter(covered_points).items() if freq >= 2])


if __name__ == "__main__":
    data = read_data("./lines_rd.txt")
    print(count_intersections(data))  # Part 1 Solution: 5632
    print(
        count_intersections(data, only_horizontal_or_vertical_line_segments=False)
    )  # Part 2 Solution: 22213
