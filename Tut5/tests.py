from typing import Any, Dict
from first_order import CORPUS, estimate_transitions, tokenise_corpus
from second_order import add_boundaries, train_second_order

EPSILON = 1e-9


def validate_cpt_normalization(model: Dict[Any, Dict[str, float]]) -> bool:
    """Verify that every row in the conditional probability table sums to 1.0."""
    for context, dist in model.items():
        prob_sum = sum(dist.values())
        if abs(prob_sum - 1.0) > EPSILON:
            return False
    return True


def test_first_order() -> bool:
    tokenized = tokenise_corpus(CORPUS)
    _, model = estimate_transitions(tokenized)
    return validate_cpt_normalization(model)


def test_second_order() -> bool:
    tokenized = add_boundaries(CORPUS)
    _, model = train_second_order(tokenized)
    return validate_cpt_normalization(model)


def main():
    t1 = test_first_order()
    t2 = test_second_order()

    print(f"First-order probability check: {'PASS' if t1 else 'FAIL'}")
    print(f"Second-order probability check: {'PASS' if t2 else 'FAIL'}")

    return t1 and t2


if __name__ == "__main__":
    main()
