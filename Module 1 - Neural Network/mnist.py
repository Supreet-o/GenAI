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


for (x_train, y_train) in train_loader:
    print("x_train:", x_train.size(), "type:", x_train.type())
    print("y_train:", y_train.size(), "type:", y_train.type())
    break

labels =[]
features = []
for X,y in zip(x_train, y_train):
  # Getting unique labels
  if y not in labels:
    labels.append(y)
    features.append(X)

print(len(features))
pltsize=1
plt.figure(figsize=(10,5))
for i in range(min(5, len(labels))):  # Safety check
    plt.subplot(1,5, i+1)
    plt.axis('off')
    plt.imshow(features[i].squeeze(), cmap="gray")  # squeeze() better than reshape
    # plt.show()
    plt.title(f'Label: {labels[i]}')

plt.show()