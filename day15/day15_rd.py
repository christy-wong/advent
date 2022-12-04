import heapq
from typing import List, Tuple

import numpy as np


def input_reader(f: str) -> np.array:
    with open(f, "r", encoding="utf-8") as f:
        lines = [list(map(int, line.rstrip())) for line in f.readlines()]
        return np.array(lines)


DATA = input_reader("./chiton_rd.txt")


class Graph:
    def __init__(self, grid: np.array):
        self._risks = {i: risk for i, risk in np.ndenumerate(grid)}
        self.start = (0, 0)
        self.end = max(self._risks, key=lambda t: t[0] + t[1])

        self.graph = {
            vertex: self._get_adjacent_vertices(vertex) for vertex in self._risks
        }
        self.min_risks = {
            vertex: float("infinity") if vertex != self.start else 0
            for vertex in self.graph
        }

    def _get_adjacent_vertices(self, vertex: Tuple[int]) -> List[Tuple[int]]:
        row, col = vertex
        potential_adjacencies = {
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        }
        return {
            adjacent: self._risks[adjacent]
            for adjacent in potential_adjacencies.intersection(self._risks)
        }

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
            # to exhaust itself (stopping condition)
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
    print(Graph(DATA).get_min_risk())  # 714
