import torch
import torch.nn as nn

torch.set_num_threads(1)

# Extended 3-class XOR dataset
X_MULTICLASS = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
], dtype=torch.float32)

Y_MULTICLASS = torch.tensor([0, 1, 1, 2], dtype=torch.long)


class ThreeClassNet(nn.Module):
    """Classifier predicting three output logits from 2D coordinates."""

    def __init__(self):
        super().__init__()
        self.encoder = nn.Linear(2, 2)
        self.head = nn.Linear(2, 3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = torch.tanh(self.encoder(x))
        return self.head(hidden)


def run_three_class_study():
    torch.manual_seed(42)

    model = ThreeClassNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

    for epoch in range(3000):
        logits = model(X_MULTICLASS)
        loss = criterion(logits, Y_MULTICLASS)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        logits = model(X_MULTICLASS)
        probabilities = torch.softmax(logits, dim=1)
        predicted_classes = torch.argmax(probabilities, dim=1)

    print("Three-Class XOR Experiment")
    print("=" * 45)
    print(f"Final training loss: {loss.item():.6f}\n")

    for sample, probs, pred in zip(
        X_MULTICLASS, probabilities, predicted_classes
    ):
        formatted_probs = [round(p.item(), 4) for p in probs]
        print(f"{sample.tolist()} -> {formatted_probs}, predicted class = {pred.item()}")

    sample_0_prob_sum = probabilities[0].sum().item()
    print(f"\nProbability sum for first example: {round(sample_0_prob_sum, 6)}")


if __name__ == "__main__":
    run_three_class_study()
