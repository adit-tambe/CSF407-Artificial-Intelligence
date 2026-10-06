# Artificial Intelligence (CSF407) — Laboratory Implementations & Solutions

> **Course:** Artificial Intelligence (CSF407)  
> **Student:** Adit Tambe  
> **BITS ID:** 2024A7PS0643G  
> **Institution:** BITS Pilani  

This repository contains independent implementations, empirical analyses, and written solutions for the Artificial Intelligence laboratory curriculum.

Each laboratory module is self-contained with its own source implementations, automated test suites, empirical outputs, and documentation.

---

## Repository Index

| Module | Topic | Core Methods & Technologies | Status |
| :--- | :--- | :--- | :---: |
| **[Tut1: Neural Models Lab](Tut1/)** | Non-Linear Representations & XOR | PyTorch, Backpropagation, Symmetry Breaking, Multi-Class Softmax | **Passed** |
| **[Tut2: Warehouse Agent](Tut2/)** | Goal-Based Reflex Navigation | Discrete 2D Grids, Breadth-First Search (BFS), Path Backtracking | **Passed** |
| **[Tut3: Search Algorithms](Tut3/)** | Informed & Uninformed Path Planning | A* Search, Manhattan & Euclidean Heuristics, Admissibility Benchmarks | **Passed** |
| **[Tut4: Logical Planning](Tut4/)** | Classical STRIPS Planning Agent | First-Order Fluents, Preconditions/Effects, Progression BFS | **Passed** |
| **[Tut5: Bayesian Networks](Tut5/)** | Probabilistic Autoregressive Models | Bigram/Trigram Markov Chains, MLE Estimation, CPT Normalization | **Passed** |

---

## Directory Architecture

```text
AI-Tutorial-Solutions/
├── Tut1/                      # Neural Models Lab
│   ├── xor_experiment.py
│   ├── symmetry_experiment.py
│   ├── activation_experiment.py
│   ├── three_class.py
│   ├── results.txt
│   └── README.md
├── Tut2/                      # Goal-Based Agent Lab
│   ├── warehouse_agent.py
│   ├── tests.py
│   ├── lab_answers.md
│   └── README.md
├── Tut3/                      # Search & A* Lab
│   ├── search_agent.py
│   ├── tests.py
│   ├── lab_answers.md
│   └── README.md
├── Tut4/                      # Logical Planning Lab
│   ├── planner.py
│   ├── tests.py
│   ├── lab_answers.md
│   └── README.md
├── Tut5/                      # Bayesian Language Models Lab
│   ├── first_order.py
│   ├── second_order.py
│   ├── tests.py
│   ├── lab_answers.md
│   └── README.md
└── README.md
```

---

## Prerequisites & Installation

The repository requires Python 3.8+ and PyTorch:

```bash
pip install torch
```

---

## Execution Guide

### Tutorial 1: Neural Models
```bash
cd Tut1
python xor_experiment.py
python symmetry_experiment.py
python activation_experiment.py
python three_class.py
```

### Tutorial 2: Warehouse Navigation Agent
```bash
cd Tut2
python warehouse_agent.py
python tests.py
```

### Tutorial 3: A* & Heuristic Search
```bash
cd Tut3
python search_agent.py
python tests.py
```

### Tutorial 4: STRIPS Planning Agent
```bash
cd Tut4
python planner.py
python tests.py
```

### Tutorial 5: Probabilistic Autoregressive Language Models
```bash
cd Tut5
python first_order.py
python second_order.py
python tests.py
```