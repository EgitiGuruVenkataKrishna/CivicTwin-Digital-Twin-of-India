import torch
from torch.utils.data import DataLoader, Dataset


class MockPostGISDataset(Dataset):
    def __init__(self, size=1000):
        self.size = size
        # Mock spatial (lat/lon as x/y) and temporal (t) grid data between 0 and 1
        self.inputs = torch.rand(size, 3)
        # Mock target values [T, AQI]
        self.targets = torch.rand(size, 2)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        return self.inputs[idx], self.targets[idx]

def get_dataloader(batch_size=32, size=1000):
    dataset = MockPostGISDataset(size=size)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
