from collections import deque
from typing import Dict, Generator, List, Optional, Tuple

# 2D Warehouse layout
DEFAULT_WAREHOUSE = [
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################",
]

# Legal cardinal movements: (action_name, delta_row, delta_col)
MOVEMENTS: List[Tuple[str, int, int]] = [
    ("Up", -1, 0),
    ("Down", 1, 0),
    ("Left", 0, -1),
    ("Right", 0, 1),
]


def find_position(grid: List[str], target_char: str) -> Optional[Tuple[int, int]]:
    """Scan the grid and return the (row, col) coordinates of target_char."""
    for r_idx, row in enumerate(grid):
        c_idx = row.find(target_char)
        if c_idx != -1:
            return (r_idx, c_idx)
    return None


def get_legal_neighbors(
    grid: List[str], position: Tuple[int, int]
) -> Generator[Tuple[str, Tuple[int, int]], None, None]:
    """Yield all legal neighboring cells along with the corresponding action."""
    r, c = position
    n_rows, n_cols = len(grid), len(grid[0])

    for action, dr, dc in MOVEMENTS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n_rows and 0 <= nc < n_cols and grid[nr][nc] != "#":
            yield action, (nr, nc)


def search(
    grid: List[str],
) -> Tuple[Optional[List[str]], Dict[Tuple[int, int], Optional[Tuple[int, int]]]]:
    """
    Perform Breadth-First Search (BFS) to find the shortest path from 'S' to 'G'.

    Returns:
        (path_actions, visited_parents)
        where path_actions is a list of direction strings, or None if unreachable.
    """
    start = find_position(grid, "S")
    goal = find_position(grid, "G")

    if not start or not goal:
        return None, {}

    queue = deque([start])
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    action_map: Dict[Tuple[int, int], str] = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for action, neighbor in get_legal_neighbors(grid, current):
            if neighbor not in parent_map:
                parent_map[neighbor] = current
                action_map[neighbor] = action
                queue.append(neighbor)

    # Goal unreachable
    if goal not in parent_map:
        return None, parent_map

    # Reconstruct route by backtracking from goal to start
    route: List[str] = []
    curr = goal
    while curr != start:
        route.append(action_map[curr])
        curr = parent_map[curr]  # type: ignore

    route.reverse()
    return route, parent_map


def format_path_coords(start: Tuple[int, int], route: List[str]) -> List[Tuple[int, int]]:
    """Convert an action route into a sequence of coordinates."""
    coords = [start]
    move_dict = {name: (dr, dc) for name, dr, dc in MOVEMENTS}
    curr = start
    for move in route:
        dr, dc = move_dict[move]
        curr = (curr[0] + dr, curr[1] + dc)
        coords.append(curr)
    return coords


def run():
    print("Warehouse Navigation - Goal Based Agent")
    print("=" * 50)

    start = find_position(DEFAULT_WAREHOUSE, "S")
    goal = find_position(DEFAULT_WAREHOUSE, "G")

    print("Environment: warehouse grid")
    print(f"Start: {start}")
    print(f"Goal: {goal}")

    route, discovered = search(DEFAULT_WAREHOUSE)

    if route is None:
        print("No valid route exists.")
        return

    print("\nPath:")
    print(" -> ".join(route))
    print("Path length:", len(route))

    coords = format_path_coords(start, route)  # type: ignore
    print("\nVisited positions in the final path:")
    print(" -> ".join(str(pos) for pos in coords))

    print(f"\nStates discovered: {len(discovered)}")


if __name__ == "__main__":
    run()
