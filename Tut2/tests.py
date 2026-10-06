from typing import List
from warehouse_agent import search


def run_test_suite():
    test_scenarios = [
        (
            "Original warehouse",
            [
                "#####################",
                "#S....#............G#",
                "#.##....##########..#",
                "#....##.............#",
                "#.######.###.#.###..#",
                "#........#..........#",
                "#####################",
            ],
            True,
        ),
        (
            "One-step warehouse",
            [
                "#####",
                "#SG.#",
                "#####",
            ],
            True,
        ),
        (
            "Unreachable goal",
            [
                "#######",
                "#S....#",
                "###.###",
                "#...#G#",
                "#######",
            ],
            False,
        ),
    ]

    print("Warehouse Agent Test Suite")
    print("=" * 40)

    all_passed = True
    for title, grid, should_find in test_scenarios:
        path, discovered = search(grid)
        found = path is not None
        passed = (found == should_find)

        if not passed:
            all_passed = False

        status = "PASS" if passed else "FAIL"
        print(f"{title:<22} {status}")
        if found:
            print(f"  Number of moves: {len(path)}")
        else:
            print("  No route was returned.")

    return all_passed


if __name__ == "__main__":
    run_test_suite()
