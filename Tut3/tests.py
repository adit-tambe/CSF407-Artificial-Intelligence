from typing import List, Optional
from search_agent import a_star, h_manhattan


def run_test_case(
    description: str,
    warehouse: List[str],
    expect_solution: bool,
    expected_steps: Optional[int] = None,
) -> bool:
    path, expanded = a_star(warehouse, h_manhattan)
    has_sol = path is not None
    passed = has_sol == expect_solution

    if passed and has_sol and expected_steps is not None:
        passed = (len(path) - 1) == expected_steps

    status = "PASS" if passed else "FAIL"
    print(f"{description}: {status}")
    if has_sol:
        print(f"  path length: {len(path) - 1}")
        print(f"  states expanded: {expanded}")

    return passed


def main():
    warehouse = [
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

    adjacent_goal = [
        "#####",
        "#SG.#",
        "#####",
    ]

    blocked_goal = [
        "#####",
        "#S#G#",
        "#####",
    ]

    print("A* Search Tests")
    print("=" * 40)

    t1 = run_test_case("Original warehouse", warehouse, True, 40)
    t2 = run_test_case("Adjacent goal", adjacent_goal, True, 1)
    t3 = run_test_case("Blocked goal", blocked_goal, False, None)

    return t1 and t2 and t3


if __name__ == "__main__":
    main()
