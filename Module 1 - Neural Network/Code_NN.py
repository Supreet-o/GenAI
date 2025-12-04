# Importing torch packages
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import torchvision
from torchvision import datasets, transforms
from torchsummary import summary
import torchvision.models as models

# Importing other packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generating a sample dataset

def graph():
    np.random.seed(0)
    X_uni = np.random.rand(100, 1) * 10  # Years of experience (between 0 and 10)
    y_uni = 3 * X_uni + 2 + np.random.randn(100, 1)  # Salary with some noise

    # print(X_uni,"x unit")
    # print(y_uni, "y unit")

    plt.scatter(X_uni,y_uni)
    plt.xlabel("year of experience")
    plt.ylabel("salary")
    plt.legend()
    plt.title("sample dataset")
    plt.show()


np.random.seed(0)
X_uni = np.random.rand(100, 1) * 10  # Years of experience (between 0 and 10)
y_uni = 3 * X_uni + 2 + np.random.randn(100, 1)  # Salary with some noise


# Convert the data to PyTorch tensors
X_uni_tensor = torch.tensor(X_uni, dtype=torch.float32)
y_uni_tensor = torch.tensor(y_uni, dtype=torch.float32)


class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1,1)

    def forward(self, x):
        return self.linear(x)
    

model = LinearRegressionModel() # linear regression model ka object bana diye hai

loss_function = nn.MSELoss() # loss function hai
optimizer = optim.SGD(model.parameters(), lr=0.01) # sgd optimizer hai

epochs = 1000 # ye epoch kitni baar train karna chahte hai existing dataset pe

for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_uni_tensor)
    loss = loss_function(outputs, y_uni_tensor)
    loss.backward() # # Loss = (wx + b - y)²
                    # d(Loss)/dw = 2*(wx + b - y)*x  # Gradient for weight
                    # d(Loss)/db = 2*(wx + b - y)    # Gradient for bias
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

model.eval()
with torch.no_grad():
    y_pred_tensor = model(X_uni_tensor)

y_pred = y_pred_tensor.numpy()


# Printing the model coefficients
bias = model.linear.bias.item()  # slope
weight = model.linear.weight.item() # weight 

print(f"Slope (Coefficient): {weight:.4f}")
print(f"Intercept: {bias:.4f}")


# Plotting the results
plt.scatter(X_uni, y_uni, color='blue', label='Original data')
plt.plot(X_uni, y_pred, color='red', label='Fitted line')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.legend()
plt.show()
