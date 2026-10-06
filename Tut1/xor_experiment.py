import torch
import torch.nn as nn

torch.set_num_threads(1)

# XOR truth table dataset
XOR_INPUTS = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
], dtype=torch.float32)

XOR_TARGETS = torch.tensor([
    [0.0],
    [1.0],
    [1.0],
    [0.0]
], dtype=torch.float32)


class XORNet(nn.Module):
    """Multi-layer perceptron for learning non-linear XOR decision boundaries."""

    def __init__(self, activation: str = "tanh"):
        super().__init__()
        self.fc1 = nn.Linear(2, 2)
        self.fc2 = nn.Linear(2, 1)

        activation_map = {
            "sigmoid": nn.Sigmoid(),
            "tanh": nn.Tanh(),
            "relu": nn.ReLU(),
        }

        if activation not in activation_map:
            raise ValueError(f"Unsupported activation function: {activation}")

        self.act = activation_map[activation]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = self.act(self.fc1(x))
        return self.fc2(hidden)


def train_xor(
    seed: int = 0,
    activation: str = "tanh",
    epochs: int = 5000,
    learning_rate: float = 0.1
):
    """Train the XOR network and record loss, gradients, and classification accuracy."""
    torch.manual_seed(seed)

    model = XORNet(activation=activation)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    initial_loss = None
    initial_w1_grad = None

    for epoch in range(epochs):
        logits = model(XOR_INPUTS)
        loss = criterion(logits, XOR_TARGETS)

        if epoch == 0:
            initial_loss = loss.item()

        optimizer.zero_grad()
        loss.backward()

        if epoch == 0:
            initial_w1_grad = model.fc1.weight.grad.detach().clone()

        optimizer.step()

    with torch.no_grad():
        final_logits = model(XOR_INPUTS)
        probabilities = torch.sigmoid(final_logits).flatten()
        predictions = (probabilities >= 0.5).to(torch.int32)

    return {
        "model": model,
        "initial_loss": initial_loss,
        "final_loss": loss.item(),
        "probabilities": probabilities,
        "predictions": predictions,
        "w1_grad": initial_w1_grad,
    }


def main():
    results = train_xor()

    print("XOR Neural Network")
    print("=" * 45)
    print("Architecture: 2 -> 2 -> 1")
    print("Hidden activation: tanh")
    print("Training loss: BCEWithLogitsLoss\n")

    print(f"Initial loss: {results['initial_loss']:.6f}")
    print(f"Final loss:   {results['final_loss']:.6f}")
    print(f"Early ||gradient W1||: {results['w1_grad'].norm().item():.6f}\n")

    print("Input       Probability    Prediction")
    for x, prob, pred in zip(
        XOR_INPUTS, results["probabilities"], results["predictions"]
    ):
        print(f"{x.tolist()}     {prob.item():.6f}       {pred.item()}")

    correct = (results["predictions"] == XOR_TARGETS.flatten().to(torch.int32)).sum().item()
    print(f"\nCorrect predictions: {correct}/4")

    print("\nFirst-layer gradient tensor from the first backward pass:")
    print(results["w1_grad"])


if __name__ == "__main__":
    main()
