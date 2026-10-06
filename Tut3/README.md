# Search Algorithms & A* Path Planning — AI Laboratory

This project provides an implementation and empirical evaluation of informed (heuristic) and uninformed state-space search algorithms for autonomous warehouse navigation, completed as part of the **Artificial Intelligence Laboratory — Search and A***.

The environment models an autonomous mobile robot tasked with calculating optimal paths through a discrete 2D grid containing corridors and static barriers. The study benchmarks Breadth-First Search (BFS) against A* using multiple admissible and inadmissible heuristic formulations.

---

## 1. Problem Representation

The navigation challenge is structured as a formal state-space search problem:

| Element | Description |
| :--- | :--- |
| **State ($s$)** | Robot grid coordinates $(r, c)$ |
| **Action Space** | Cardinal movements: `Up`, `Down`, `Left`, `Right` |
| **Step Cost ($c$)** | Uniform cost of $1.0$ per transition |
| **Start State ($S$)** | Marked by origin token `S` |
| **Goal State ($G$)** | Marked by target token `G` |
| **Constraints** | Out-of-bounds transitions and barrier cells (`#`) are strictly prohibited |

---

## 2. Search Algorithms

### Breadth-First Search (BFS)
Uninformed search exploring outward level-by-level using a FIFO queue. It guarantees path length optimality when transition costs are uniform.

### A* Heuristic Search
Informed search that orders the priority queue (min-heap) according to the evaluation function:
$$f(n) = g(n) + h(n)$$
where:
* $g(n)$ is the exact accumulated path cost from the origin to node $n$.
* $h(n)$ is an estimated lower bound of the cost from node $n$ to the destination.
* $f(n)$ is the projected total path cost passing through node $n$.

---

## 3. Heuristic Formulations & Analysis

Four heuristic configurations are evaluated:

1. **Manhattan Distance ($h_{\text{manhattan}}$):**
   $$h(n) = |r_n - r_g| + |c_n - c_g|$$
   *Admissible & Consistent* for 4-connected grid movement without diagonal traversal.

2. **Zero Heuristic ($h(n) = 0$):**
   Reduces $f(n) = g(n)$, turning A* into Uniform Cost Search (Dijkstra's Algorithm).

3. **Euclidean Distance ($h_{\text{euclidean}}$):**
   $$h(n) = \sqrt{(r_n - r_g)^2 + (c_n - c_g)^2}$$
   *Admissible*, measuring straight-line distance, but less informed than Manhattan for orthogonal grids.

4. **Inflated Manhattan ($h(n) = 2 \times h_{\text{manhattan}}$):**
   Deliberately breaks admissibility ($h(n) \not\le h^*(n)$). Explores aggressively toward the target at the risk of sub-optimality.

---

## 4. Execution & Testing

### Running Comparative Experiments
Run the primary benchmarking suite:
```bash
python search_agent.py
```

The script reports path existence, optimal path length, coordinate trajectories, and node expansion counts for all five configurations.

### Running Automated Test Assertions
Run the test suite verifying edge cases and ground truths:
```bash
python tests.py
```

Test cases covered:
* Full benchmark maze (confirms optimal 40-step path).
* Adjacent goal base case (confirms 1-step direct exit).
* Fully barricaded goal (confirms safe frontier exhaustion and `None` return).

---

## 5. Repository Structure

```text
Tut3/
├── search_agent.py   # BFS and A* engines with pluggable heuristics
├── tests.py          # Automated verification suite
├── lab_answers.md    # Detailed theoretical and empirical lab answers
├── README.md         # Technical overview and mathematical formulation
└── .gitignore        # Git ignore file
```
