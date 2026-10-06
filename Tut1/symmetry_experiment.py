import torch
import torch.nn as nn

torch.set_num_threads(1)

# XOR truth table inputs and labels
DATA = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
], dtype=torch.float32)

LABELS = torch.tensor([
    [0.0],
    [1.0],
    [1.0],
    [0.0]
], dtype=torch.float32)


class ZeroInitNet(nn.Module):
    """Network used to study symmetry when initialized with zero weights."""

    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 2)
        self.output = nn.Linear(2, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.sigmoid(self.hidden(x))
        return self.output(h)


def run_symmetry_study():
    net = ZeroInitNet()

    # Explicitly initialize all weights and biases to zero
    with torch.no_grad():
        for param in net.parameters():
            param.fill_(0.0)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.5)

    print("Symmetry Experiment")
    print("=" * 45)
    print("Hidden weights at initialization:")
    print(net.hidden.weight)

    for step in range(5):
        logits = net(DATA)
        loss = criterion(logits, LABELS)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"\nAfter update {step + 1}:")
        print(net.hidden.weight)

    print("\nObservation:")
    print("Both hidden neurons continue to have identical weights.")
    print(
        "Since they start with the same parameters and receive the same "
        "gradients, training does not break the symmetry between them."
    )


if __name__ == "__main__":
    run_symmetry_study()