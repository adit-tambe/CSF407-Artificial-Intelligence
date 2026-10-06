# Laboratory Answers — Goal-Based Navigation Agent

## Task 1: Goal-Based Agent Specification

### 1. Environment
The environment is a discrete, two-dimensional spatial grid representing a warehouse. Each coordinate is either traversable (`.`), obstructed by an impassable barrier (`#`), designated as the initial start (`S`), or designated as the target destination (`G`). The world is fully observable, static, and deterministic.

### 2. Goal
The agent's objective is to determine a collision-free trajectory of valid single-step movements that transitions the robot from its initial coordinate `S` to the destination coordinate `G`.

### 3. Available Actions
The agent possesses four discrete cardinal navigation actions:
* **`Up`**: $(-1, 0)$
* **`Down`**: $(+1, 0)$
* **`Left`**: $(0, -1)$
* **`Right`**: $(0, +1)$

Each action has a uniform transition cost of $1$ unit. Actions attempting to move through walls (`#`) or outside the grid bounds are illegal.

### 4. Search State & Information Maintained
To plan an effective trajectory, the agent tracks:
* The current spatial state $(r, c)$.
* A frontier queue of discovered states waiting for expansion.
* An `explored` / `parent_map` mapping each discovered cell to its immediate predecessor and the action taken. This serves two vital roles: preventing infinite loops caused by revisits, and enabling backwards path reconstruction from `G` to `S`.

### 5. Why this is a Goal-Based Agent
A simple reflex agent selects actions based entirely on immediate sensory percepts (e.g., "if wall ahead, turn right"). In contrast, this agent maintains an explicit internal representation of a target destination (`G`). It searches through prospective future state trajectories and selects an action sequence specifically because it leads to achieving the goal condition.

### Additional Consideration
Breadth-First Search (BFS) exhibits $O(b^d)$ time and space complexity, where $b$ is the branching factor and $d$ is the solution depth. In massive or unbounded environments, maintaining all frontier nodes in memory becomes prohibitive, motivating informed heuristic search (e.g., A*) or memory-bounded algorithms (IDA*).

---

## Task 2: Agent Architecture

The agent's operational lifecycle is structured as follows:

```text
       Warehouse Grid Environment
                   │
                   ▼
         Extract Start & Goal
                   │
                   ▼
         Initialize BFS Frontier
                   │
         ┌─────────┴─────────┐
         ▼                   │
   Pop Next State            │
         │                   │
         ▼                   │
   Goal Reached? ──Yes──► Reconstruct Path & Return
         │                   │
         No                  │
         │                   │
         ▼                   │
   Generate Legal Neighbors  │
         │                   │
         ▼                   │
   Filter Visited/Walls      │
         │                   │
         ▼                   │
   Enqueue Successors ───────┘
```

The search engine systematically generates candidate state transitions, while the goal test governs termination.

---

## Task 3: Empirical Testing & Validation

The test suite evaluates three distinct warehouse layouts:

1. **Original Warehouse:** Complex layout with corridors and obstacles. The agent discovers an optimal route of **20 moves** after expanding 63 states.
2. **One-Step Warehouse:** Minimal adjacent layout where `G` is directly adjacent to `S`. Successfully yields a 1-step direct route.
3. **Unreachable Goal:** Completely enclosed destination surrounded by barriers. The agent exhausts the reachable frontier and terminates safely returning `None`, proving that it does not loop infinitely or hallucinate non-existent routes.

---

## LLM-Based Engineering Reflection

### Program Verification
Code generated or drafted with LLM assistance must never be assumed correct without formal validation. The implementation was verified through strict test assertions, checking both path feasibility (all intermediate steps are legal) and optimality (minimal step count).

### Prompt Precision
To produce dependable AI systems, prompts must provide exact environmental specifications:
* Precise grid representation and symbol definitions.
* Legal action primitives and boundary conditions.
* Expected return data types for both success and failure cases.
* Specific test scenarios and invariant constraints.

### Selection of Search Strategy
**Breadth-First Search (BFS)** was chosen because all movement actions carry uniform step costs ($c = 1$). Under this property, BFS is guaranteed to discover the shortest path in terms of total actions while avoiding the unnecessary overhead of priority queue sorting.
