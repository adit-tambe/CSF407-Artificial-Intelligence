# Laboratory Answers — Bayesian Networks & Autoregressive Sequence Models

## 1. Why Factorize Sequences with the Probability Chain Rule?
By the fundamental probability chain rule, the joint probability of any sequence of tokens $W = (w_1, w_2, \dots, w_T)$ is factored as:
$$P(w_1, w_2, \dots, w_T) = \prod_{t=1}^T P(w_t \mid w_1, w_2, \dots, w_{t-1})$$
This decomposition transforms the intractable problem of modeling the joint distribution over all conceivable sentences into a step-by-step next-token prediction task. It provides a principled mathematical framework for autoregressive text generation.

---

## 2. The First-Order Markov Assumption
A first-order autoregressive model applies the Markov property, asserting that the distribution of the next token depends exclusively on the immediately preceding token:
$$P(w_t \mid w_1, w_2, \dots, w_{t-1}) = P(w_t \mid w_{t-1})$$
All historical tokens prior to $w_{t-1}$ are assumed conditionally independent of $w_t$.

---

## 3. Empirical Conditional Distributions
Using the 6-sentence laboratory corpus, Maximum Likelihood Estimation yields:

* **Given context `"the"`:**
  * $P(\text{cat} \mid \text{the}) = 0.250$
  * $P(\text{dog} \mid \text{the}) = 0.250$
  * $P(\text{mat} \mid \text{the}) = 0.167$
  * $P(\text{rug} \mid \text{the}) = 0.167$
  * $P(\text{park} \mid \text{the}) = 0.167$
* **Given context `"cat"` & `"dog"`:**
  * $P(\text{sat} \mid \text{cat}) = 0.667$, $P(\text{ran} \mid \text{cat}) = 0.333$
  * $P(\text{sat} \mid \text{dog}) = 0.667$, $P(\text{ran} \mid \text{dog}) = 0.333$
* **Deterministic Transitions:**
  * $P(\text{on} \mid \text{sat}) = 1.000$
  * $P(\text{to} \mid \text{ran}) = 1.000$

Any unobserved bigram receives empirical probability $0.0$.

---

## 4. Internal Representation of Transition Frequencies
Transition statistics are maintained using a nested hash structure:
```python
defaultdict(Counter)
```
The outer key represents the conditioning context $w_{t-1}$, and the inner `Counter` tallies observed transitions to successor tokens $w_t$.

---

## 5. Construction of Conditional Probability Tables (CPTs)
For every context $c$, the conditional probability assigned to token $w$ is the relative frequency:
$$P(w \mid c) = \frac{C(c, w)}{\sum_{w' \in V} C(c, w')}$$
Normalizing across all outgoing transition counts ensures each row forms a valid categorical probability distribution.

---

## 6. Decoding Strategies: Greedy vs. Stochastic Sampling
* **Greedy Decoding:** At each timestep, selects the mode:
  $$w_t^* = \arg\max_{w} P(w \mid w_{t-1})$$
  Because the argmax decision is purely deterministic, greedy decoding with a fixed seed and context always yields the identical sequence. On small cyclic corpora, it can trap the generator in an infinite repeating loop (e.g., `"the cat sat on the cat sat on..."`).
* **Stochastic Sampling:** Draws $w_t \sim P(\cdot \mid w_{t-1})$. Every token with non-zero probability has a chance of selection proportional to its likelihood, creating diverse, non-repetitive sentence trajectories across runs.

---

## 7. Handling Unobserved Contexts
If the generator encounters a token with no recorded outgoing transitions in the training set (an absorbing state or out-of-vocabulary context), the conditional distribution is undefined ($\emptyset$). The generator terminates generation and safely emits the accumulated string.

---

## 8. Diagnosis of Invalid Probability Sums
By Kolmogorov's probability axioms, the sum of probabilities across the sample space of possible successors must strictly equal 1:
$$\sum_{w \in V} P(w \mid c) = 1.0$$
If an estimated row sums to a deviant value such as `0.87`, it signals a bug in normalization, uncounted transitions, or float truncation errors.

---

## 9. Model Statistics vs. Human Linguistic Expectation
The model relies entirely on empirical co-occurrence frequencies within the 6 training sentences. It possesses no latent semantic representations, syntax parsing, or commonsense world models. Consequently, continuations that are grammatically or commonsensically obvious to a human (e.g., `"the cat drank the milk"`) have zero probability under this model.

---

## 10. Why Sampling Generates Diverse Text
Greedy decoding collapses the search space onto the single local maximum at each step. In contrast, stochastic sampling explores the full probabilistic support of the conditional distribution, allowing lower-probability branches (such as `"dog"` or `"rug"`) to be selected, generating different valid sentences across runs.

---

## 11. Characteristics of a Second-Order Model
A second-order autoregressive model extends the conditioning context to a 2-token tuple:
$$P(w_t \mid w_{t-2}, w_{t-1})$$
* Conditioning contexts are bigrams $(w_{t-2}, w_{t-1})$.
* Requires $V^2$ potential conditional distributions.
* Captures higher-order syntactic agreement (e.g., distinguishing whether `"the"` was preceded by `"on"` or `"to"`).

---

## 12. Context Size Tradeoff: Expressivity vs. Data Sparsity
Expanding context size ($N$-gram order) incorporates richer historical information, resolving local ambiguities. However, the number of possible contexts grows exponentially with $O(|V|^{N-1})$. On small datasets, most contexts are never observed, causing severe data sparsity where the model either overfits to verbatim training sentences or fails on unseen prefixes.

---

## 13. Mathematical Rigor in Probabilistic Modeling
Formalizing the model mathematically ensures:
* Verifiable invariants (e.g., row-sum normalization $\sum P = 1.0$).
* Clear separation between training (MLE estimation) and inference (sampling vs. argmax).
* Predictable behavior during edge cases and missing transitions.

---

## 14. Bayesian Network Interpretation
Viewing an autoregressive language model as a Bayesian network reveals:
* **Topology:** A directed acyclic graph (DAG) where nodes represent sequence positions $X_1, X_2, \dots, X_T$, and edges encode causal temporal conditioning.
* **CPTs:** Each node $X_t$ contains a Conditional Probability Table parameterizing $P(X_t \mid \text{Parents}(X_t))$.
* **Factorization:** The joint probability factorizes directly into the product of local conditional distributions, illustrating that autoregressive sequence modeling is a dynamic Bayesian network.
