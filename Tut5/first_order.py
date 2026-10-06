import random
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

CORPUS: List[str] = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


def tokenise_corpus(lines: List[str]) -> List[List[str]]:
    """Tokenize sentences in lowercase and wrap with explicit sequence boundaries."""
    tokenized = []
    for line in lines:
        words = line.strip().lower().split()
        tokenized.append(["<START>", *words, "<END>"])
    return tokenized


def estimate_transitions(
    tokenised_sentences: List[List[str]],
) -> Tuple[Dict[str, Counter], Dict[str, Dict[str, float]]]:
    """
    Compute first-order bigram transition frequencies and normalized CPTs.

    P(X_t = next | X_{t-1} = previous) = Count(previous, next) / Count(previous)
    """
    counts: Dict[str, Counter] = defaultdict(Counter)

    for sentence in tokenised_sentences:
        for prev_tok, next_tok in zip(sentence[:-1], sentence[1:]):
            counts[prev_tok][next_tok] += 1

    distributions: Dict[str, Dict[str, float]] = {}
    for prev_tok, next_counts in counts.items():
        total_transitions = sum(next_counts.values())
        distributions[prev_tok] = {
            tok: count / total_transitions for tok, count in next_counts.items()
        }

    return dict(counts), distributions


def greedy_choice(
    distributions: Dict[str, Dict[str, float]], context: str
) -> Optional[str]:
    """Select the argmax token with highest conditional probability."""
    options = distributions.get(context)
    if not options:
        return None
    return max(options, key=options.get)  # type: ignore


def random_choice(
    distributions: Dict[str, Dict[str, float]], context: str
) -> Optional[str]:
    """Sample the next token according to the conditional probability distribution."""
    options = distributions.get(context)
    if not options:
        return None
    tokens = list(options.keys())
    weights = list(options.values())
    return random.choices(tokens, weights=weights, k=1)[0]


def generate_text(
    distributions: Dict[str, Dict[str, float]],
    deterministic: bool = False,
    limit: int = 20,
) -> str:
    """Generate a sentence autoregressively until <END> or step limit."""
    context = "<START>"
    tokens: List[str] = []

    for _ in range(limit):
        if deterministic:
            next_token = greedy_choice(distributions, context)
        else:
            next_token = random_choice(distributions, context)

        if next_token is None or next_token == "<END>":
            break

        tokens.append(next_token)
        context = next_token

    return " ".join(tokens)


def display_distributions(
    distributions: Dict[str, Dict[str, float]], contexts: List[str]
):
    """Print formatted conditional probability tables."""
    for ctx in contexts:
        print(f"\nP(next | {ctx})")
        if ctx not in distributions:
            print("  no recorded transitions")
            continue
        for tok, prob in sorted(distributions[ctx].items()):
            print(f"  {tok:8s}: {prob:.3f}")


def main():
    random.seed(7)

    dataset = tokenise_corpus(CORPUS)
    counts, probabilities = estimate_transitions(dataset)

    print("First-order autoregressive model")
    print("=" * 50)

    display_distributions(
        probabilities, ["the", "cat", "dog", "sat", "ran"]
    )

    print("\nConditional probability checks")
    for context, distribution in probabilities.items():
        total = sum(distribution.values())
        print(f"{context:8s}: {total:.3f}")

    print("\nGreedy next-token predictions")
    for context in ["the", "cat", "dog", "sat", "ran"]:
        print(f"{context:8s} -> {greedy_choice(probabilities, context)}")

    print("\nGreedy generation")
    for _ in range(5):
        print(generate_text(probabilities, deterministic=True))

    print("\nSampling generation")
    for _ in range(20):
        print(generate_text(probabilities))


if __name__ == "__main__":
    main()
