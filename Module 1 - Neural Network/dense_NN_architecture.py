import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import torchvision
from torchvision import datasets, transforms
from torchsummary import summary
import torchvision.models as models

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,)),])

mnist_trainset = datasets.MNIST(root="./data", train=True, download = True, transform=transform)
train_loader = torch.utils.data.DataLoader(dataset=mnist_trainset, batch_size=20, shuffle=True)

mnist_testset = datasets.MNIST(root="./root", transform=transform, download=True)
test_loader = torch.utils.data.DataLoader(dataset=mnist_testset, batch_size=20, shuffle=True)


class Model(nn.modules):
    def __init__(self):
        self.fc1 = nn.Linear(28 * 28, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28) # Flatten the image
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        x = F.log_softmax(x, dim=1)
        
        return x
        
