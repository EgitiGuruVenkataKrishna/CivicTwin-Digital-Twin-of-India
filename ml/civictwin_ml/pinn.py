import math

import torch
import torch.nn as nn


class CivicTwinPINN(nn.Module):
    def __init__(self, in_features: int = 3, hidden_dim: int = 64, out_features: int = 2, dropout_p: float = 0.1):
        super().__init__()

        # Fourier Feature Embedding for spatial (lat/lon) and temporal (t) inputs
        self.B = nn.Parameter(torch.randn(in_features, hidden_dim // 2) * 10.0, requires_grad=False)

        # 4-layer MLP backbone
        self.net = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout_p),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout_p),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout_p),
            nn.Linear(hidden_dim, out_features)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape is expected to be [batch_size, 3] for (x, y, t)
        x_proj = 2.0 * math.pi * torch.matmul(x, self.B)
        x_ff = torch.cat([torch.sin(x_proj), torch.cos(x_proj)], dim=-1)

        # Output is [T, AQI]
        out = self.net(x_ff)
        return out
