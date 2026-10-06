from collections import deque
from typing import FrozenSet, Iterable, List, Optional, Set


class Action:
    """Represents a STRIPS-style planning operator with preconditions and effects."""

    def __init__(
        self,
        label: str,
        requires: Optional[Iterable[str]] = None,
        forbids: Optional[Iterable[str]] = None,
        adds: Optional[Iterable[str]] = None,
        removes: Optional[Iterable[str]] = None,
    ):
        self.label = label
        self.requires: Set[str] = set(requires or ())
        self.forbids: Set[str] = set(forbids or ())
        self.adds: Set[str] = set(adds or ())
        self.removes: Set[str] = set(removes or ())

    def applicable(self, state: FrozenSet[str]) -> bool:
        """Verify that positive preconditions hold and forbidden fluents are absent."""
        return self.requires.issubset(state) and self.forbids.isdisjoint(state)

    def execute(self, state: FrozenSet[str]) -> FrozenSet[str]:
        """Apply the transition function: S' = (S \\ removes) U adds."""
        updated = set(state)
        updated.difference_update(self.removes)
        updated.update(self.adds)
        return frozenset(updated)

    def __repr__(self) -> str:
        return f"<Action {self.label}>"


def plan_with_bfs(
    start_state: Iterable[str],
    action_list: List[Action],
    target: Iterable[str],
) -> Optional[List[Action]]:
    """
    Forward state-space search (progression planning) using Breadth-First Search.

    Returns:
        List of Action steps achieving the goal, or None if unsolvable.
    """
    initial_frozenset = frozenset(start_state)
    target_set = set(target)

    if target_set.issubset(initial_frozenset):
        return []

    # Queue contains tuples of (current_state, accumulated_action_plan)
    frontier = deque([(initial_frozenset, [])])
    explored: Set[FrozenSet[str]] = {initial_frozenset}

    while frontier:
        state, plan = frontier.popleft()

        for action in action_list:
            if not action.applicable(state):
                continue

            successor = action.execute(state)

            if successor in explored:
                continue

            extended_plan = plan + [action]

            if target_set.issubset(successor):
                return extended_plan

            explored.add(successor)
            frontier.append((successor, extended_plan))

    return None


def warehouse_actions(
    allow_pickup_at_a: bool = True,
    add_wait_action: bool = False,
) -> List[Action]:
    """Construct the standard STRIPS domain actions for the warehouse problem."""
    movement_actions = [
        Action(
            "Move(A, B)",
            requires={"At(Robot,A)"},
            adds={"At(Robot,B)"},
            removes={"At(Robot,A)"},
        ),
        Action(
            "Move(B, A)",
            requires={"At(Robot,B)"},
            adds={"At(Robot,A)"},
            removes={"At(Robot,B)"},
        ),
        Action(
            "Move(B, C)",
            requires={"At(Robot,B)"},
            adds={"At(Robot,C)"},
            removes={"At(Robot,B)"},
        ),
        Action(
            "Move(C, B)",
            requires={"At(Robot,C)"},
            adds={"At(Robot,B)"},
            removes={"At(Robot,C)"},
        ),
    ]

    pickup_actions: List[Action] = []
    if allow_pickup_at_a:
        pickup_actions.append(
            Action(
                "PickUp(Package, A)",
                requires={"At(Robot,A)", "At(Package,A)"},
                adds={"Holding(Package)"},
                removes={"At(Package,A)"},
            )
        )

    pickup_actions.extend([
        Action(
            "PickUp(Package, B)",
            requires={"At(Robot,B)", "At(Package,B)"},
            adds={"Holding(Package)"},
            removes={"At(Package,B)"},
        ),
        Action(
            "PickUp(Package, C)",
            requires={"At(Robot,C)", "At(Package,C)"},
            adds={"Holding(Package)"},
            removes={"At(Package,C)"},
        ),
    ])

    drop_actions = [
        Action(
            "Drop(Package, A)",
            requires={"At(Robot,A)", "Holding(Package)"},
            adds={"At(Package,A)"},
            removes={"Holding(Package)"},
        ),
        Action(
            "Drop(Package, B)",
            requires={"At(Robot,B)", "Holding(Package)"},
            adds={"At(Package,B)"},
            removes={"Holding(Package)"},
        ),
        Action(
            "Drop(Package, C)",
            requires={"At(Robot,C)", "Holding(Package)"},
            adds={"At(Package,C)"},
            removes={"Holding(Package)"},
        ),
    ]

    all_actions = movement_actions + pickup_actions + drop_actions

    if add_wait_action:
        all_actions.append(
            Action(
                "Wait(A)",
                requires={"At(Robot,A)"},
                adds={"At(Robot,A)"},
            )
        )

    return all_actions


def simulate(
    start: Iterable[str], plan: List[Action]
) -> Optional[List[FrozenSet[str]]]:
    """Execute a plan step-by-step and track the trajectory of states."""
    curr = frozenset(start)
    trajectory = [curr]

    for action in plan:
        if not action.applicable(curr):
            return None
        curr = action.execute(curr)
        trajectory.append(curr)

    return trajectory


def display_solution(initial: Iterable[str], plan: Optional[List[Action]]):
    if plan is None:
        print("No plan found.")
        return

    history = simulate(initial, plan)
    if history is None:
        print("Plan execution failed!")
        return

    print("\nPlan:")
    for idx, act in enumerate(plan, 1):
        print(f"{idx}. {act.label}")

    print("\nState sequence:")
    for idx, state in enumerate(history):
        print(f"S{idx}: {sorted(state)}")

    goal_met = "At(Package,C)" in history[-1]
    print("\nGoal achieved:", goal_met)


def main():
    initial_state = {"At(Robot,A)", "At(Package,A)"}
    target_goal = {"At(Package,C)"}
    actions = warehouse_actions()

    print("Logical Planning Agent")
    print("=" * 50)

    plan = plan_with_bfs(initial_state, actions, target_goal)
    display_solution(initial_state, plan)


if __name__ == "__main__":
    main()
