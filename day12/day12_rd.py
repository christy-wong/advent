from collections import defaultdict
from typing import Dict, Set, List


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


def paths_finder(
    graph: Dict[str, Set[str]], start: str, end: str, path=[]
) -> List[List[str]]:
    """
    Returns list of paths (each path a list) from `start` to `end`
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
        if node.isupper() or (node.islower() and (node not in path)):
            new_paths = paths_finder(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)

    return paths


if __name__ == "__main__":
    graph = read_data("./caves_rd.txt")
    print(len(paths_finder(graph, 'start', 'end')))  # Part 1 Solution: 4338
