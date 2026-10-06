import random
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

SAMPLES: List[str] = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


def add_boundaries(sentences: List[str]) -> List[List[str]]:
    """Tokenize and pad with two start markers to initialize a second-order context."""
    sequences = []
    for text in sentences:
        tokens = text.strip().lower().split()
        sequences.append(["<START>", "<START>", *tokens, "<END>"])
    return sequences


def train_second_order(
    sequences: List[List[str]],
) -> Tuple[Dict[Tuple[str, str], Counter], Dict[Tuple[str, str], Dict[str, float]]]:
    """
    Train second-order trigram transitions:
    P(X_t = next | X_{t-2} = w1, X_{t-1} = w2)
    """
    counts: Dict[Tuple[str, str], Counter] = defaultdict(Counter)

    for tokens in sequences:
        for idx in range(2, len(tokens)):
            history = (tokens[idx - 2], tokens[idx - 1])
            target = tokens[idx]
            counts[history][target] += 1

    model: Dict[Tuple[str, str], Dict[str, float]] = {}
    for history, next_counts in counts.items():
        total = sum(next_counts.values())
        model[history] = {
            tok: count / total for tok, count in next_counts.items()
        }

    return dict(counts), model


def choose_greedy(
    model: Dict[Tuple[str, str], Dict[str, float]], history: Tuple[str, str]
) -> Optional[str]:
    """Deterministically choose the argmax continuation."""
    distribution = model.get(history)
    if not distribution:
        return None
    return max(distribution, key=distribution.get)  # type: ignore


def choose_sample(
    model: Dict[Tuple[str, str], Dict[str, float]], history: Tuple[str, str]
) -> Optional[str]:
    """Sample according to categorical probability weights."""
    distribution = model.get(history)
    if not distribution:
        return None
    candidates = list(distribution.keys())
    probabilities = list(distribution.values())
    return random.choices(candidates, weights=probabilities, k=1)[0]


def generate(
    model: Dict[Tuple[str, str], Dict[str, float]],
    deterministic: bool = False,
    maximum: int = 20,
) -> str:
    """Generate text autoregressively using a 2-token sliding context window."""
    history = ("<START>", "<START>")
    generated: List[str] = []

    for _ in range(maximum):
        if deterministic:
            token = choose_greedy(model, history)
        else:
            token = choose_sample(model, history)

        if token is None or token == "<END>":
            break

        generated.append(token)
        history = (history[1], token)

    return " ".join(generated)


def show_distribution(
    model: Dict[Tuple[str, str], Dict[str, float]], history: Tuple[str, str]
):
    """Display conditional probability distribution for a specific 2-token context."""
    print(f"\nP(next | {history})")
    distribution = model.get(history, {})
    for token, probability in sorted(distribution.items()):
        print(f"  {token:8s}: {probability:.3f}")


def main():
    random.seed(11)

    sequences = add_boundaries(SAMPLES)
    counts, model = train_second_order(sequences)

    print("Second-order autoregressive model")
    print("=" * 50)

    examples = [
        ("the", "cat"),
        ("the", "dog"),
        ("cat", "ran"),
        ("dog", "sat"),
        ("sat", "on"),
    ]

    for history in examples:
        show_distribution(model, history)

    print("\nConditional probability checks")
    for history, distribution in model.items():
        total = sum(distribution.values())
        print(f"{history}: {total:.3f}")

    print("\nSampled sentences")
    for _ in range(10):
        print(generate(model))


if __name__ == "__main__":
    main()
