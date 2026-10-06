import torch
import torch.nn as nn

torch.set_num_threads(1)

X_DATA = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
], dtype=torch.float32)

Y_DATA = torch.tensor([0, 1, 1, 0], dtype=torch.long)


class ActivationBenchmarkNet(nn.Module):
    """Two-layer network supporting configurable non-linear activation."""

    def __init__(self, activation_fn: nn.Module):
        super().__init__()
        self.fc1 = nn.Linear(2, 2)
        self.fc2 = nn.Linear(2, 1)
        self.act = activation_fn

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(self.act(self.fc1(x)))


def benchmark_activations():
    activations = {
        "sigmoid": nn.Sigmoid(),
        "tanh": nn.Tanh(),
        "relu": nn.ReLU(),
    }

    seeds = {
        "sigmoid": 1,
        "tanh": 0,
        "relu": 2,
    }

    print("Activation Experiment")
    print("=" * 45)

    for name, act_fn in activations.items():
        seed = seeds[name]
        torch.manual_seed(seed)

        model = ActivationBenchmarkNet(act_fn)
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

        early_grad_norm = None

        for epoch in range(5000):
            logits = model(X_DATA)
            loss = criterion(logits, Y_DATA.float().unsqueeze(1))

            optimizer.zero_grad()
            loss.backward()

            if epoch == 0:
                early_grad_norm = model.fc1.weight.grad.norm().item()

            optimizer.step()

        with torch.no_grad():
            probs = torch.sigmoid(model(X_DATA)).flatten()
            preds = (probs >= 0.5).to(torch.int32)

        correct = (preds == Y_DATA.to(torch.int32)).sum().item()

        print(
            f"{name:8s} "
            f"loss={loss.item():.6f} "
            f"correct={correct}/4 "
            f"early_grad={early_grad_norm:.6f}"
        )
        print("  probabilities:", [round(p.item(), 4) for p in probs])


if __name__ == "__main__":
    benchmark_activations()
