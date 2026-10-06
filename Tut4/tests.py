from typing import Iterable, List, Set
from planner import Action, plan_with_bfs, simulate, warehouse_actions


def run_planning_test(
    title: str,
    initial: Set[str],
    goal: Set[str],
    actions: List[Action],
    expect_solution: bool,
) -> bool:
    plan = plan_with_bfs(initial, actions, goal)
    has_plan = plan is not None
    passed = has_plan == expect_solution

    if passed and has_plan:
        history = simulate(initial, plan)
        passed = history is not None and goal.issubset(history[-1])

    status = "PASS" if passed else "FAIL"
    print(f"{title}: {status}")
    if plan is not None:
        print("  Plan:", [act.label for act in plan])

    return passed


def main():
    initial_state = {"At(Robot,A)", "At(Package,A)"}
    goal_state = {"At(Package,C)"}

    print("Planning Agent Test Suite")
    print("=" * 40)

    t1 = run_planning_test(
        "Test A - solvable warehouse",
        initial_state,
        goal_state,
        warehouse_actions(),
        True,
    )

    t2 = run_planning_test(
        "Test B - pickup unavailable",
        initial_state,
        goal_state,
        warehouse_actions(allow_pickup_at_a=False),
        False,
    )

    t3 = run_planning_test(
        "Test C - irrelevant action",
        initial_state,
        goal_state,
        warehouse_actions(add_wait_action=True),
        True,
    )

    return t1 and t2 and t3


if __name__ == "__main__":
    main()
