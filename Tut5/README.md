# Bayesian Networks & Autoregressive Language Models

This project implements discrete probabilistic sequence models and investigates their connection to Bayesian networks and autoregressive generative modeling. It was created as part of the **Artificial Intelligence Laboratory — Bayesian Networks & Sequence Models**.

The models are trained via Maximum Likelihood Estimation (MLE) on a toy text corpus, comparing first-order ($N=2$) and second-order ($N=3$) Markov models, greedy versus stochastic text decoding, and conditional probability table (CPT) normalization.

---

## Dataset

The training set comprises 6 canonical animal locomotion sentences:
```text
the cat sat on the mat
the cat sat on the rug
the dog sat on the mat
the dog ran to the park
the cat ran to the park
the dog sat on the rug
```

Sentences are converted to lowercase and wrapped with `<START>` and `<END>` boundary tokens to formally model sequence initiation and termination distributions.

---

## Model Formulations

### First-Order Model (Bigram)
Assumes the next token depends solely on the immediate predecessor:
$$P(X_t \mid X_1, \dots, X_{t-1}) = P(X_t \mid X_{t-1})$$
Transition counts are normalized as:
$$P(w_{\text{next}} \mid w_{\text{prev}}) = \frac{C(w_{\text{prev}}, w_{\text{next}})}{\sum_{w'} C(w_{\text{prev}}, w')}$$

### Second-Order Model (Trigram)
Conditions on a sliding history window of two prior tokens:
$$P(X_t \mid X_1, \dots, X_{t-1}) = P(X_t \mid X_{t-2}, X_{t-1})$$
The context space consists of ordered bigram pairs $(w_{t-2}, w_{t-1})$.

---

## Text Generation Strategies

1. **Deterministic Greedy Decoding:**
   $$w_t = \arg\max_{w} P(w \mid \text{context})$$
   Always follows the single highest-probability trajectory. May produce cyclical loops on small corpora.

2. **Categorical Stochastic Sampling:**
   Draws tokens randomly according to the conditional probability distribution. Generates diverse, valid linguistic combinations across repeated runs.

---

## Execution & Verification

### Running First-Order Experiments
```bash
python first_order.py
```
Reports:
* CPT distributions for key words (`the`, `cat`, `dog`, etc.)
* Row-sum normalization checks
* Greedy sequence generation
* 20 sample stochastic sentences

### Running Second-Order Experiments
```bash
python second_order.py
```
Reports:
* Trigram conditional probability tables
* Trigram row-sum checks
* 10 sample generated sentences with enhanced grammatical coherence

### Running Probability Invariant Tests
```bash
python tests.py
```
Validates that every row in the learned conditional probability tables across both models sums strictly to $1.0 \pm 10^{-9}$.

---

## First-Order vs. Second-Order Comparison

| Dimension | First-Order ($N=2$) | Second-Order ($N=3$) |
| :--- | :--- | :--- |
| **Conditioning History** | 1 token | 2 tokens |
| **Context Cardinality** | $|V|$ | $|V|^2$ potential contexts |
| **Context Disambiguation** | Low (blends distinct usages) | High (separates preposition contexts) |
| **Data Sparsity Risk** | Minimal | High (many zero-frequency bigrams) |
| **Training Data Requirement** | Small | Substantially larger |

---

## Directory Structure

```text
Tut5/
├── first_order.py    # First-order bigram model and generation engine
├── second_order.py   # Second-order trigram model and generation engine
├── tests.py          # Strict CPT probability normalization test suite
├── lab_answers.md    # In-depth theoretical and empirical lab answers
├── README.md         # Technical overview and Bayesian formulation
└── .gitignore        # Git ignore file
```
