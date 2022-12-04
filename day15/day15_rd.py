import heapq
from typing import List, Tuple

import numpy as np


def input_reader(f: str) -> np.array:
    with open(f, "r", encoding="utf-8") as f:
        lines = [list(map(int, line.rstrip())) for line in f.readlines()]
        return np.array(lines)


def augment_cave(tile: np.array) -> np.array:
    tile_width, tile_height = tile.shape
    full_cave = np.tile(tile, (5, 5))
    tile_incr = np.vectorize(lambda r: (r % 9) + ((r % 9 == 0) * 9))
    for i in range(5):
        for j in range(5):
            x, y = i * tile_height, j * tile_width
            full_cave[x : x + tile_height, y : y + tile_width] = tile_incr(
                tile + (i + j)
            )
    return full_cave


DATA = input_reader("./chiton_rd.txt")
DATA2 = augment_cave(DATA)


class Graph:
    def __init__(self, grid: np.array):
        self._grid = grid
        self._risks = {i: risk for i, risk in np.ndenumerate(self._grid)}
        self.start = (0, 0)
        self.end = self._grid.shape[0] - 1, self._grid.shape[1] - 1
        self.graph = {
            vertex: self._get_adjacent_vertices(vertex) for vertex in self._risks
        }
        self.min_risks = {
            vertex: float("infinity") if vertex != self.start else 0
            for vertex in self.graph
        }

    def _get_adjacent_vertices(self, vertex: Tuple[int]) -> List[Tuple[int]]:
        row, col = vertex
        adjacencies = list(
            filter(
                lambda t: t[0] >= 0
                and t[1] >= 0
                and t[0] <= self.end[0]
                and t[1] <= self.end[1],
                [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)],
            )
        )
        return {adjacent: self._risks[adjacent] for adjacent in adjacencies}

    def get_min_risk(self) -> int:
        """
        Return minimum risk to the end of the grid via implementation of Djikstra's
        algorithm with min-heap
        """
        visited = set()
        pq = [(0, self.start)]
        while pq:
            current_risk, current_vertex = heapq.heappop(pq)
            # NOTE: This is a very important condition for the priority queue
            # to exhaust itself; a node isn't explored more than once even if
            # added to the queue multiple times
            if current_vertex in visited:
                continue
            for neighbor, neighbor_risk in self.graph[current_vertex].items():
                self.min_risks[neighbor] = min(
                    current_risk + neighbor_risk, self.min_risks[neighbor]
                )
                heapq.heappush(pq, (self.min_risks[neighbor], neighbor))
            visited.add(current_vertex)
        return self.min_risks[self.end]


if __name__ == "__main__":
    small_cave, big_cave = Graph(DATA), Graph(DATA2)
    print(small_cave.get_min_risk())  # 714
    print(big_cave.get_min_risk())  # 2948
