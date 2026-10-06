import heapq
from collections import deque
from typing import Callable, Dict, Generator, List, Optional, Tuple

# 9x17 Benchmark Warehouse Layout
WAREHOUSE_MAP = [
    "#################",
    "#S....#.........#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#.............#G#",
    "#################",
]

CARDINAL_STEPS: Tuple[Tuple[int, int], ...] = (
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
)


def find_marker(grid: List[str], marker: str) -> Tuple[int, int]:
    """Locate the row and column of a marker in the grid."""
    for r_idx, row in enumerate(grid):
        c_idx = row.find(marker)
        if c_idx != -1:
            return r_idx, c_idx
    raise ValueError(f"Marker '{marker}' not found in grid.")


def get_adjacent(
    grid: List[str], pos: Tuple[int, int]
) -> Generator[Tuple[int, int], None, None]:
    """Yield all passable adjacent coordinates."""
    r, c = pos
    n_rows, n_cols = len(grid), len(grid[0])

    for dr, dc in CARDINAL_STEPS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n_rows and 0 <= nc < n_cols and grid[nr][nc] != "#":
            yield nr, nc


def reconstruct_path(
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
    target: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """Trace parent links from target back to origin."""
    path = []
    curr: Optional[Tuple[int, int]] = target
    while curr is not None:
        path.append(curr)
        curr = parent_map.get(curr)
    path.reverse()
    return path


def h_manhattan(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    """Manhattan distance heuristic: |dr| + |dc|."""
    return float(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))


def h_euclidean(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    """Euclidean distance heuristic: sqrt(dr^2 + dc^2)."""
    return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5


def a_star(
    grid: List[str],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = h_manhattan,
    scale: float = 1.0,
) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    Execute A* search using f(n) = g(n) + scale * h(n).

    Returns:
        (optimal_path, states_expanded)
    """
    start = find_marker(grid, "S")
    goal = find_marker(grid, "G")

    # Priority queue storing: (f_score, tie_breaker_seq, coordinate)
    frontier: List[Tuple[float, int, Tuple[int, int]]] = []
    seq = 0
    heapq.heappush(frontier, (0.0, seq, start))

    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}
    expanded_count = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        expanded_count += 1

        if current == goal:
            return reconstruct_path(parent_map, goal), expanded_count

        for neighbor in get_adjacent(grid, current):
            tentative_g = g_cost[current] + 1
            recorded_g = g_cost.get(neighbor)

            if recorded_g is not None and tentative_g >= recorded_g:
                continue

            g_cost[neighbor] = tentative_g
            parent_map[neighbor] = current

            f_score = tentative_g + scale * heuristic(neighbor, goal)
            seq += 1
            heapq.heappush(frontier, (f_score, seq, neighbor))

    return None, expanded_count


def breadth_first_search(
    grid: List[str],
) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """Execute standard uninformed BFS for baseline comparison."""
    start = find_marker(grid, "S")
    goal = find_marker(grid, "G")

    queue = deque([start])
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    expanded_count = 0

    while queue:
        current = queue.popleft()
        expanded_count += 1

        if current == goal:
            return reconstruct_path(parent_map, goal), expanded_count

        for neighbor in get_adjacent(grid, current):
            if neighbor not in parent_map:
                parent_map[neighbor] = current
                queue.append(neighbor)

    return None, expanded_count


def print_search_report(label: str, result: Tuple[Optional[List[Tuple[int, int]]], int]):
    path, expanded = result
    print(label)
    print("-" * 40)
    if path is None:
        print("Solution found: No")
    else:
        print("Solution found: Yes")
        print("Path length:", len(path) - 1)
        print("Path:", path)
    print("States expanded:", expanded)
    print()


def main():
    print("Warehouse Search: BFS and A*")
    print("=" * 50)

    configs = [
        ("BFS", lambda: breadth_first_search(WAREHOUSE_MAP)),
        ("A* Manhattan", lambda: a_star(WAREHOUSE_MAP, h_manhattan, 1.0)),
        ("A* h(n)=0", lambda: a_star(WAREHOUSE_MAP, scale=0.0)),
        ("A* Euclidean", lambda: a_star(WAREHOUSE_MAP, h_euclidean, 1.0)),
        ("A* Manhattan x2", lambda: a_star(WAREHOUSE_MAP, h_manhattan, 2.0)),
    ]

    for title, run_fn in configs:
        print_search_report(title, run_fn())


if __name__ == "__main__":
    main()
