# Neural Models Laboratory — XOR & Representations

This repository contains the complete implementation and empirical analysis for the Neural Models laboratory session conducted on **August 7, 2026**.

The primary objective is to investigate the foundational mechanics of artificial neural networks using the canonical XOR (Exclusive-OR) problem. Specifically, the lab explores:
1. Why linear models fail on non-linearly separable functions and why non-linear hidden representations are necessary.
2. The formulation of output layers and loss functions for binary classification using numerically stable logits (`BCEWithLogitsLoss`).
3. Weight initialization and the symmetry-breaking problem.
4. The comparative impact of activation functions (`tanh`, `sigmoid`, `ReLU`) on gradient flow and training dynamics.
5. Multi-class generalization with softmax normalization and cross-entropy loss.
6. The mechanics of automatic differentiation and backpropagation in PyTorch.

---

## Environment & Requirements

The scripts are implemented in Python 3 with minimal external dependencies:
* `python >= 3.8`
* `torch >= 2.0`

---

## Directory Structure

```text
Tut1/
├── xor_experiment.py         # Standard XOR network with tanh hidden units
├── symmetry_experiment.py     # Zero-weight initialization and symmetry persistence
├── activation_experiment.py   # Benchmark of Sigmoid, Tanh, and ReLU activations
├── three_class.py             # 3-class classification extension with Softmax
├── results.txt                # Consolidated console outputs from all runs
└── README.md                  # Comprehensive laboratory documentation
```

---

## 1. XOR Binary Classification

### Problem Formulation
The XOR truth table defines a classic non-linearly separable problem:

| $x_1$ | $x_2$ | Target $y$ |
| :---: | :---: | :--------: |
|   0   |   0   |     0      |
|   0   |   1   |     1      |
|   1   |   0   |     1      |
|   1   |   1   |     0      |

No single hyper-plane $w_1 x_1 + w_2 x_2 + b = 0$ can separate $(0,1), (1,0)$ from $(0,0), (1,1)$.

### Network Architecture
We employ a Multi-Layer Perceptron (MLP):
$$\mathbf{h} = \tanh(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$$
$$\hat{y}_{\text{logit}} = \mathbf{w}_2^\top \mathbf{h} + b_2$$

* **Input Dimension:** 2
* **Hidden Neurons:** 2 (sufficient to map inputs to a linearly separable 2D feature space)
* **Output:** 1 logit passed to `torch.nn.BCEWithLogitsLoss`, which internally computes:
$$\mathcal{L} = - [y \log(\sigma(\hat{y})) + (1 - y) \log(1 - \sigma(\hat{y}))]$$
using the log-sum-exp trick to avoid numerical underflow.

### Execution
```bash
python xor_experiment.py
```

The script trains the model using Adam ($\text{lr} = 0.1$) for 5,000 iterations, reporting:
* Initial loss: `0.715159`
* Final loss: `0.000011`
* Test accuracy: `4/4 (100%)`
* First-layer gradient tensor $\nabla_{\mathbf{W}_1} \mathcal{L}$ during step 1.

---

## 2. Weight Initialization & Symmetry

### The Symmetry Problem
When all weights $\mathbf{W}$ and biases $\mathbf{b}$ are initialized to zero:
1. For any input $\mathbf{x}$, all hidden units receive identical pre-activations $z_1 = z_2 = 0$.
2. The hidden activations are identical: $h_1 = h_2 = \sigma(0)$.
3. During backpropagation, the gradients with respect to each hidden neuron's weights are identical:
$$\frac{\partial \mathcal{L}}{\partial w_{1j}} = \frac{\partial \mathcal{L}}{\partial w_{2j}}$$
4. As a result, standard gradient descent updates each hidden unit identically at every step. The neurons cannot specialize to detect distinct features.

### Execution
```bash
python symmetry_experiment.py
```
This experiment initializes every trainable parameter to $0.0$ and applies SGD updates ($\text{lr} = 0.5$). Across all 5 iterations, `hidden.weight` remains strictly row-identical, demonstrating why random symmetry-breaking initialization is essential.

---

## 3. Activation Functions Comparison

We benchmark three non-linear activations under identical training conditions:
1. **Sigmoid:** $\sigma(z) = \frac{1}{1 + e^{-z}}$ (bounded $[0, 1]$, saturates at extremes)
2. **Tanh:** $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ (zero-centered $[-1, 1]$, steeper gradients)
3. **ReLU:** $\text{ReLU}(z) = \max(0, z)$ (non-saturating for positive inputs)

### Execution
```bash
python activation_experiment.py
```

### Empirical Results
* **`sigmoid`**: Loss $= 0.000026$, Accuracy $= 4/4$, Early Gradient Norm $= 0.004304$
* **`tanh`**: Loss $= 0.000011$, Accuracy $= 4/4$, Early Gradient Norm $= 0.061785$
* **`relu`**: Loss $= 0.000004$, Accuracy $= 4/4$, Early Gradient Norm $= 0.004868$

`tanh` exhibits significantly larger initial gradient flow due to zero-centered outputs and a maximal derivative of $1.0$ at $z=0$, compared to $0.25$ for sigmoid.

---

## 4. Multi-Class Classification Extension

The XOR input space is mapped to three distinct classes:
* $(0, 0) \to \text{Class } 0$
* $(0, 1) \to \text{Class } 1$
* $(1, 0) \to \text{Class } 1$
* $(1, 1) \to \text{Class } 2$

### Architecture & Loss
The final layer outputs three unnormalized logits $[\hat{z}_0, \hat{z}_1, \hat{z}_2]$. We train using `CrossEntropyLoss()`:
$$\mathcal{L} = -\log \left( \frac{e^{\hat{z}_y}}{\sum_{j=0}^2 e^{\hat{z}_j}} \right)$$

### Execution
```bash
python three_class.py
```
* Final training loss converges to `0.000015`.
* Probabilities are evaluated using softmax and verified to sum to $1.000000$ for all inputs.

---

## 5. Backpropagation Mechanics in PyTorch

The standard training step follows the directed acyclic computation graph:
1. **Forward Pass:** `outputs = model(inputs)`
2. **Objective Evaluation:** `loss = criterion(outputs, targets)`
3. **Gradient Clearance:** `optimizer.zero_grad()`
4. **Backward Accumulation:** `loss.backward()` (populates `.grad` attributes via the chain rule)
5. **Parameter Step:** `optimizer.step()`

PyTorch's automatic differentiation engine (`torch.autograd`) allows inspection of weight gradients directly via `model.fc1.weight.grad`.

---

## Summary of Results

All outputs from our experiment runs are cataloged in [`results.txt`](file:///c:/Users/adits/Downloads/AI%20Tutorials%20Repo/AI-Tutorial-Solutions/Tut1/results.txt).
