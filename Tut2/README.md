# Goal-Based Warehouse Navigation Agent

This project implements a goal-directed navigation agent for an autonomous vehicle operating in a discrete two-dimensional warehouse environment. It was constructed as part of the **Agents Laboratory — Constructing a Goal-Based Agent**.

The agent receives a grid map containing an initial origin (`S`), a designated destination (`G`), and static obstacles (`#`). It systematically computes an optimal, collision-free action sequence to reach the destination using Breadth-First Search (BFS).

---

## Environment Specification

The warehouse is represented as an ASCII matrix:

| Symbol | Description                 | Passable |
| :----: | :-------------------------- | :------: |
|  `S`   | Starting origin             |   Yes    |
|  `G`   | Target destination          |   Yes    |
|  `#`   | Obstacle / perimeter wall   |    No    |
|  `.`   | Open traversable aisle      |   Yes    |

### Action Primitives
The agent can execute four unit-step orthogonal movements:
* **Up:** $(-1, 0)$
* **Down:** $(+1, 0)$
* **Left:** $(0, -1)$
* **Right:** $(0, +1)$

---

## Agent Architecture & Search Design

The agent is designed as a **Goal-Based Agent**. Unlike reflex architectures, its decisions are governed by explicit consideration of future states toward a specified target goal state.

### Breadth-First Search (BFS)
Because every step incurs a uniform cost ($c=1$), BFS guarantees the discovery of an optimal (shortest) path. The search operates as follows:

```text
Initialize Queue with S ──► Pop Front State ──► Check Goal Condition
                                  │
                                  ▼
                         Expand Legal Neighbors
                                  │
                                  ▼
                    Filter Visited Cells & Walls
                                  │
                                  ▼
                    Enqueue & Record Predecessors
```

### Route Reconstruction
During expansion, a predecessor dictionary records `parent_map[child] = parent` and `action_map[child] = action`. Once the target coordinate `G` is reached, the route is reconstructed by following parent links back to `S` and reversing the accumulated list.

---

## Execution & Testing

### Running the Agent
Run the primary warehouse navigation demo:
```bash
python warehouse_agent.py
```

The script outputs:
* Start and goal coordinates
* Step-by-step action sequence
* Full coordinate path trajectory
* Number of visited and discovered states

### Running the Test Suite
Execute the automated test suite:
```bash
python tests.py
```

The test suite validates:
1. **Default Warehouse:** Confirms path finding succeeds with the optimal length of 20 moves.
2. **One-Step Map:** Verifies immediate goal recognition.
3. **Unreachable Destination:** Ensures safe termination when no path exists without infinite loops.

---

## Project Structure

```text
Tut2/
├── warehouse_agent.py   # Core BFS search algorithm and agent definition
├── tests.py             # Multi-scenario automated test cases
├── lab_answers.md       # Detailed answers to laboratory questions
├── README.md            # Technical documentation
└── .gitignore           # Git ignore file
```
