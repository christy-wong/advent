from collections import Counter, defaultdict
from typing import Dict, List, Set


def read_data(raw_data_file: str) -> Dict[str, Set[str]]:
    """
    Reads data into dictionary mapping node to other reachable nodes
    """
    data = defaultdict(set)
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            node_1, node_2 = line.split("-")
            data[node_1].add(node_2)
            data[node_2].add(node_1)
    return data


def can_visit_small_cave_again(
    graph: Dict[str, Set[str]], node: str, path: List[str], condition: str = "Part 1"
):
    """
    Returns boolean whether a small cave/`node` can be revisited or not
    depending on `condition`
    """
    node_visited_counter = Counter(path)
    revisited_fewer_than_twice = [
        node_visited_counter[node] < 2
        for node in node_visited_counter
        if node.islower()
    ]
    revisited_exactly_twice = [
        node_visited_counter[node] == 2
        for node in node_visited_counter
        if node.islower()
    ]

    # Conditions for returning to small cave
    if condition == "Part 1":
        return node not in path
    elif condition == "Part 2":
        return node != "start" and (
            all(revisited_fewer_than_twice)
            or ((sum(revisited_exactly_twice) == 1) and (node not in path))
        )
    else:
        raise ValueError("Invalid `condition`")

    return False


def paths_finder(
    graph: Dict[str, Set[str]], start: str, end: str, path=[], condition="Part 1"
) -> List[List[str]]:
    """
    Returns list of paths (each `path` itself a list) from `start` to `end`
    """
    path = path + [start]

    # Base case(s)
    if start == end:
        return [path]
    if start not in graph:
        return []

    paths = []

    # Recursive case(s)
    for node in graph[start]:
        if node.isupper() or can_visit_small_cave_again(graph, node, path, condition):
            new_paths = paths_finder(graph, node, end, path, condition)
            for new_path in new_paths:
                paths.append(new_path)

    return paths


if __name__ == "__main__":
    graph = read_data("./caves_rd.txt")
    print(len(paths_finder(graph, "start", "end")))  # Part 1 Solution: 4338
    print(
        len(paths_finder(graph, "start", "end", condition="Part 2"))
    )  # Part 2 Solution: 114189
