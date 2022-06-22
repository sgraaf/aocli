import heapq
from collections import defaultdict
from typing import Any, Optional, Sequence, Union

inf = float("inf")


def find_dimensions_2d(grid: Sequence[Sequence[Any]]) -> tuple[int, int]:
    return len(grid), max(len(item) for item in grid)


def find_neighbouring_indices_2d(
    i: int,
    j: int,
    bounds_i: Optional[tuple[int, int]] = None,
    bounds_j: Optional[tuple[int, int]] = None,
    include_diagonals: bool = False,
) -> list[tuple[int, int]]:
    all_bounds = (bounds_i, bounds_j)
    if any(all_bounds) and not all(
        all_bounds
    ):  # make sure all bounds are specified (or none)
        raise ValueError(
            "When specifying bounds, you must specify bounds for both dimentions (i and j)."
        )
    neighbouring_indices = []
    for di, dj in [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]:
        if include_diagonals or not (di and dj):
            i_ = i + di
            j_ = j + dj
            if bounds_i is not None and bounds_j is not None:
                min_i, max_i = bounds_i
                min_j, max_j = bounds_j
                if (
                    min_i <= i_ <= max_i - 1 and min_j <= j_ <= max_j - 1
                ):  # check for bounds
                    neighbouring_indices.append((i_, j_))
            else:
                neighbouring_indices.append((i_, j_))
    return neighbouring_indices


def find_dimensions_3d(grid: Sequence[Sequence[Sequence[Any]]]) -> tuple[int, int, int]:
    return (
        len(grid),
        max(len(item) for item in grid),
        max(len(sub_item) for item in grid for sub_item in item),
    )


def find_neighbouring_indices_3d(
    i: int,
    j: int,
    k: int,
    bounds_i: Optional[tuple[int, int]] = None,
    bounds_j: Optional[tuple[int, int]] = None,
    bounds_k: Optional[tuple[int, int]] = None,
    include_diagonals: bool = False,
) -> list[tuple[int, int, int]]:
    all_bounds = (bounds_i, bounds_j, bounds_k)
    if any(all_bounds) and not all(
        all_bounds
    ):  # make sure all bounds are specified (or none)
        raise ValueError(
            "When specifying bounds, you must specify bounds for all dimentions (i, j and k)."
        )
    neighbouring_indices = []
    for di, dj, dk in [
        (i, j, k)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        for k in (-1, 0, 1)
        if not (i == j == k == 0)
    ]:
        if include_diagonals or not sum(map(bool, (di, dj, dk))) > 1:
            i_ = i + di
            j_ = j + dj
            k_ = k + dk
            if bounds_i is not None and bounds_j is not None and bounds_k is not None:
                # unpack bounds
                min_i, max_i = bounds_i
                min_j, max_j = bounds_j
                min_k, max_k = bounds_k
                if (
                    min_i <= i_ <= max_i - 1
                    and min_j <= j_ <= max_j - 1
                    and min_k <= k_ <= max_k - 1
                ):  # check for bounds
                    neighbouring_indices.append((i_, j_, k_))
            else:
                neighbouring_indices.append((i_, j_, k_))
    return neighbouring_indices


def find_dimensions_4d(
    grid: Sequence[Sequence[Sequence[Sequence[Any]]]],
) -> tuple[int, int, int, int]:
    return (
        len(grid),
        max(len(item) for item in grid),
        max(len(sub_item) for item in grid for sub_item in item),
        max(
            len(sub_sub_item)
            for item in grid
            for sub_item in item
            for sub_sub_item in sub_item
        ),
    )


def find_neighbouring_indices_4d(
    i: int,
    j: int,
    k: int,
    l: int,
    bounds_i: Optional[tuple[int, int]] = None,
    bounds_j: Optional[tuple[int, int]] = None,
    bounds_k: Optional[tuple[int, int]] = None,
    bounds_l: Optional[tuple[int, int]] = None,
    include_diagonals: bool = False,
) -> list[tuple[int, int, int, int]]:
    all_bounds = (bounds_i, bounds_j, bounds_k, bounds_l)
    if any(all_bounds) and not all(
        all_bounds
    ):  # make sure all bounds are specified (or none)
        raise ValueError(
            "When specifying bounds, you must specify bounds for all dimentions (i, j, k and l)."
        )
    neighbouring_indices = []
    for di, dj, dk, dl in [
        (i, j, k, l)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        for k in (-1, 0, 1)
        for l in (-1, 0, 1)
        if not (i == j == k == l == 0)
    ]:
        if include_diagonals or not sum(map(bool, (di, dj, dk, dl))) > 1:
            i_ = i + di
            j_ = j + dj
            k_ = k + dk
            l_ = l + dl
            if (
                bounds_i is not None
                and bounds_j is not None
                and bounds_k is not None
                and bounds_l is not None
            ):
                # unpack bounds
                min_i, max_i = bounds_i
                min_j, max_j = bounds_j
                min_k, max_k = bounds_k
                min_l, max_l = bounds_l
                if (
                    min_i <= i_ <= max_i - 1
                    and min_j <= j_ <= max_j - 1
                    and min_k <= k_ <= max_k - 1
                    and min_l <= l_ <= max_l - 1
                ):  # check for bounds
                    neighbouring_indices.append((i_, j_, k_, l_))
            else:
                neighbouring_indices.append((i_, j_, k_, l_))
    return neighbouring_indices


class Graph:
    def __init__(self) -> None:
        self.edges: dict[
            tuple[int, int], list[tuple[tuple[int, int], int]]
        ] = defaultdict(list)
        self.vertices: set[tuple[int, int]] = set()

    def add_edge(self, u: tuple[int, int], v: tuple[int, int], weight: int) -> None:
        self.edges[u].append((v, weight))
        self.vertices.add(u)
        self.vertices.add(v)

    def dijkstra(
        self, source: tuple[int, int], dest: Optional[tuple[int, int]] = None
    ) -> Union[float, dict[tuple[int, int], float]]:
        D: dict[tuple[int, int], float] = {v: inf for v in self.vertices}
        D[source] = 0

        queue: list[tuple[int, tuple[int, int]]] = [(0, source)]
        visited: set[tuple[int, int]] = set()

        while queue:
            (dist, v) = heapq.heappop(queue)

            if dest is not None and v == dest:
                return dist

            if v in visited:
                continue

            for neighbour, weight in self.edges[v]:
                old_weight = D[neighbour]
                new_weight = D[v] + weight
                if new_weight < old_weight:
                    heapq.heappush(queue, (new_weight, neighbour))  # type: ignore
                    D[neighbour] = new_weight

            visited.add(v)

        return inf if dest is not None else D
