# Search and A* — Laboratory Answers

## Task 0: Formal Search Problem Formulation

The warehouse navigation task is formalized as a classical state-space search problem:

| Component | Formal Definition | Warehouse Specification |
| :--- | :--- | :--- |
| **State Space ($\mathcal{S}$)** | Coordinate location of the robot | Discrete tuples $(r, c) \in \{0 \dots H-1\} \times \{0 \dots W-1\}$ |
| **Action Space ($\mathcal{A}$)** | Applicable directional displacements | $\mathcal{A} = \{\text{Up}, \text{Down}, \text{Left}, \text{Right}\}$ |
| **Transition Function ($T$)** | Deterministic transition $T(s, a) \to s'$ | $(r + \Delta r, c + \Delta c)$ if passable, else undefined |
| **Initial State ($s_0$)** | Point of departure | Coordinate matching marker `S` |
| **Goal Condition ($G$)** | Objective test | Coordinate matching marker `G` |
| **Path Cost ($c$)** | Cumulative step penalty | Unit cost: $c(s, a, s') = 1$ for all valid moves |

### Analytical Questions
* **(a) State Representation:** Since the robot has no orientation or load status in this exercise, $(r, c)$ coordinates completely specify the state.
* **(b) Invalid Transitions:** Transitions into coordinates where $\text{grid}[r][c] = \text{'#'}$ or indices outside the bounding matrix are pruned from the successor set.
* **(c) Determinism:** The environment is strictly deterministic; executing action $a$ from state $s$ invariably leads to the unique successor $s'$.
* **(d) Solution Definition:** A finite sequence of legal actions $\langle a_1, a_2, \dots, a_k \rangle$ transitioning the agent along path $\langle s_0, s_1, \dots, s_k \rangle$ such that $s_k = G$.

---

## Task 4: Structural Analysis of the A* Engine

The implementation organizes search elements as follows:

| Search Component | Code Construct | Operational Role |
| :--- | :--- | :--- |
| **Frontier** | Python `heapq` (min-heap) | Stores unexpanded candidate nodes sorted by $f(n)$ |
| **Priority Metric** | $f(n) = g(n) + h(n)$ | Balances cost incurred so far with estimated remaining cost |
| **Cost-so-far** | `g_cost` dictionary | Tracks the cheapest known path cost from start to state $n$ |
| **Predecessors** | `parent_map` dictionary | Maintains back-pointers for optimal route reconstruction |
| **Tie-Breaker** | Sequence counter integer | Preserves strict FIFO determinism when $f$-scores collide |

### Detailed Questions
* **(a) Frontier Representation:** A binary min-heap populated with tuples $(f(n), \text{seq}, \text{state})$.
* **(b) Node Selection:** The node with the minimal estimated total cost $f(n) = \min_{u \in \text{Frontier}} [g(u) + h(u)]$ is popped first.
* **(c) Heuristic Origin:** Computed analytically from geometric coordinates relative to the goal ($h_{\text{manhattan}}$ or $h_{\text{euclidean}}$).
* **(d) Explicit $f(n)$ Calculation:** Yes; for every candidate successor, $f(n) = g(n) + \text{scale} \times h(n)$ is computed prior to heap insertion.
* **(e) Role of `g_cost` Dictionary:** Acts as an exploration barrier. If a newly discovered path to state $n$ is more expensive than or equal to an existing entry in `g_cost`, the successor is skipped, preventing redundant cyclic re-expansions.

---

## Task 5: Empirical Comparison — Uninformed (BFS) vs. Informed (A*)

Both BFS and A* discover the optimal path of **40 moves** on the benchmark map.

* **BFS:** Expands 64 states, sweeping outward uniformly in concentric cost rings.
* **A* (Manhattan):** Expands 65 states, steering exploration toward the goal.
* **Path Trajectory:** Both algorithms return identical optimal 40-step paths navigating the narrow labyrinth corridors.

In tightly constrained corridor maps with dead ends and barriers, heuristic estimates may temporarily guide nodes toward obstacle walls before backtracking, demonstrating that heuristic efficiency depends heavily on obstacle topology.

---

## Task 6: Heuristic Analysis & Admissibility

Four heuristic variants were evaluated:

### 1. Zero Heuristic ($h(n) = 0$)
* **Mechanism:** Reduces $f(n) = g(n)$, making A* identical to Uniform Cost Search (Dijkstra's Algorithm).
* **Observed Metrics:** Path length = 40, States expanded = 64.

### 2. Euclidean Distance ($h_2(n) = \sqrt{\Delta r^2 + \Delta c^2}$)
* **Mechanism:** Measures straight-line geometric distance.
* **Admissibility:** Strictly admissible because straight-line distance is always $\le$ grid travel distance. However, it is less informed (strictly dominates less) than Manhattan distance for 4-connected grid movement ($h_{\text{euclidean}} \le h_{\text{manhattan}}$).
* **Observed Metrics:** Path length = 40, States expanded = 65.

### 3. Standard Manhattan Distance ($h_1(n) = |\Delta r| + |\Delta c|$)
* **Mechanism:** Exact minimum step distance ignoring obstacles.
* **Admissibility & Consistency:** Both admissible ($h(n) \le h^*(n)$) and consistent ($h(n) \le c(n, n') + h(n')$), guaranteeing that the first time a goal node is expanded, the path is optimal.
* **Observed Metrics:** Path length = 40, States expanded = 65.

### 4. Overestimating Heuristic ($h(n) = 2 \times \text{Manhattan}$)
* **Mechanism:** Inflates the heuristic estimate beyond the true minimum cost.
* **Admissibility Violation:** Because $h(n)$ can exceed the true shortest remaining cost $h^*(n)$, admissibility is broken. A* effectively degrades toward Greedy Best-First Search.
* **Risk:** While often expanding fewer nodes in open spaces, it forfeits the theoretical guarantee of optimality and can return suboptimal paths in complex mazes. In this corridor map, it expanded 68 states.

---

## Task 7: Validation & Reflection

### Test Case Coverage
* **Benchmark Warehouse:** Asserts that the full maze yields the optimal 40-step path.
* **Adjacent Goal (1 step):** Confirms base-case termination without unnecessary exploration.
* **Completely Blocked Goal:** Confirms termination with empty/None solution upon frontier exhaustion.

### Engineering & LLM Insights
Algorithmic code requires formal invariant testing. Heuristic search code can appear functional while silently violating optimality if tie-breaking, heap ordering, or re-opening logic is flawed. Automated assertion testing against known ground truths is necessary to confirm algorithmic correctness.
