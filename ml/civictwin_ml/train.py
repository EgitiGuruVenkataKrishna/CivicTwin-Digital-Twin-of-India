import os

import torch
import torch.nn as nn
import torch.optim as optim

from civictwin_ml.data_loader import get_dataloader
from civictwin_ml.losses import composite_loss, heat_diffusion_residual
from civictwin_ml.pinn import CivicTwinPINN


def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = CivicTwinPINN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    dataloader = get_dataloader(batch_size=64, size=1000)
    mse_criterion = nn.MSELoss()

    epochs = 10
    lambda_weight = 0.05

    model.train()

    for epoch in range(epochs):
        epoch_loss = 0.0
        for inputs, targets in dataloader:
            inputs = inputs.to(device)
            targets = targets.to(device)

            # Split inputs into x, y, t and require gradients for PDE loss
            x = inputs[:, 0:1].clone().requires_grad_(True)
            y = inputs[:, 1:2].clone().requires_grad_(True)
            t = inputs[:, 2:3].clone().requires_grad_(True)

            # Recombine to pass to model
            pinn_inputs = torch.cat([x, y, t], dim=1)

            optimizer.zero_grad()
            outputs = model(pinn_inputs)

            # MSE loss against mocked ground truth
            mse_loss = mse_criterion(outputs, targets)

            # PDE loss for Temperature (T is the first output)
            T = outputs[:, 0:1]
            pde_res = heat_diffusion_residual(T, x, y, t)
            pde_loss = torch.mean(pde_res**2)

            # Composite loss
            loss = composite_loss(mse_loss, pde_loss, lambda_weight)

            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(dataloader):.4f}")

    # Ensure directory exists before saving model
    export_dir = os.path.join(os.path.dirname(__file__), '..', 'hf_space', 'model')
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, 'pinn_v1.pt')

    # Export model with TorchScript
    model.eval()
    example_input = torch.randn(1, 3, device=device)
    scripted_model = torch.jit.trace(model, example_input)
    scripted_model.save(export_path)
    print(f"Model saved to {export_path}")

if __name__ == '__main__':
    train()
