# Logical Planning Agent — STRIPS Planning Domain

This project implements a forward state-space progression planner (STRIPS-style) for an autonomous mobile logistics robot, developed for the **Artificial Intelligence Laboratory — Logical Planning**.

The planner formulates navigation, acquisition, and delivery tasks in terms of formal state logic, action preconditions, and add/delete effect sets. It synthesizes valid action sequences using Breadth-First Search (BFS).

---

## Warehouse Planning Domain

The logistics environment consists of three interconnected spatial zones:
$$\text{Locations: } A \longleftrightarrow B \longleftrightarrow C$$

### State Predicates (Fluents)
* `At(Robot, <loc>)`: The current location of the mobile unit.
* `At(Package, <loc>)`: The resting location of the package.
* `Holding(Package)`: True if the mobile unit is carrying the package.

### Initial & Goal States
* **Initial State ($S_0$):** `{"At(Robot, A)", "At(Package, A)"}`
* **Target Goal ($G$):** `{"At(Package, C)"}`

---

## Action Representation

Each action schema is encapsulated in the `Action` class with four explicit sets of ground literals:
* **`requires`:** Positive preconditions that must belong to the current state ($S \models \text{requires}$).
* **`forbids`:** Negative preconditions that must NOT belong to the current state ($S \cap \text{forbids} = \emptyset$).
* **`removes`:** Delete list of fluents negated by executing the action.
* **`adds`:** Add list of fluents asserted by executing the action.

The state transition function evaluates:
$$S' = (S \setminus \text{removes}) \cup \text{adds}$$

---

## Planning Algorithm

We utilize **Forward State-Space Search (Progression Planning)**:
1. Initialize a FIFO frontier with $(S_0, \langle \rangle)$.
2. Dequeue state $S$ and test if $G \subseteq S$.
3. For all domain actions, filter those whose preconditions hold in $S$.
4. Generate successor states $S'$ via transition updates.
5. Record unexplored states to avoid cyclical planning.
6. Reconstruct the action sequence upon finding a state satisfying $G$.

Because all actions have unit step costs, BFS guarantees finding the minimum-length plan.

---

## Execution & Verification

### Running the Planner
Execute the primary planning demonstration:
```bash
python planner.py
```

Outputs the synthesized 4-step plan:
```text
1. PickUp(Package, A)
2. Move(A, B)
3. Move(B, C)
4. Drop(Package, C)
```
along with the intermediate ground state progression $S_0 \to S_1 \to S_2 \to S_3 \to S_4$.

### Running the Test Suite
Execute automated test scenarios:
```bash
python tests.py
```

Validates:
* **Test A (Solvable Domain):** Synthesizes optimal plan achieving `At(Package, C)`.
* **Test B (No PickUp):** Confirms planner correctly detects impossibility and returns `None`.
* **Test C (Irrelevant Action):** Introduces a benign `Wait(A)` action, confirming the planner ignores distractions and preserves plan optimality.

---

## Project Structure

```text
Tut4/
├── planner.py       # Action definitions, BFS progression planner, and simulation
├── tests.py         # Multi-condition scenario testing
├── lab_answers.md   # Detailed theoretical reflections and question responses
├── README.md        # Technical specifications and STRIPS logic guide
└── .gitignore       # Git ignore file
```
