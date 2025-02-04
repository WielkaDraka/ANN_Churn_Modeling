# -*- coding: utf-8 -*-
"""Artificial_neural_network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-AGiw-ysHT0xfZktReavZ7MGkLLUZu26

# Artificial Neural Network

### Importing the libraries
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:-1].values
y = dataset.iloc[:, -1].values

print(X)

print(y)

"""### Encoding categorical data

Label Encoding the "Gender" column
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])

print(X)

"""One Hot Encoding the "Geography" column"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Part 2 - Building the ANN

### Defining the model
"""

class ANNModel(nn.Module):
    def __init__(self):
        super(ANNModel, self).__init__()
        self.layer1 = nn.Linear(12, 12)  # Input layer to first hidden layer
        self.layer2 = nn.Linear(12, 6)   # First hidden layer to second hidden layer
        self.output = nn.Linear(6, 1)   # Second hidden layer to output layer

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = torch.sigmoid(self.output(x))
        return x

model = ANNModel()

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

"""### Training the ANN on the Training set"""

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

num_epochs = 100
batch_size = 32
num_batches = len(X_train) // batch_size

for epoch in range(num_epochs):
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        X_batch = X_train_tensor[start:end]
        y_batch = y_train_tensor[start:end]

        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

"""## Part 4 - Making the predictions and evaluating the model

### Predicting the result of a single observation
"""

single_obs = np.array([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])
single_obs_scaled = sc.transform(single_obs)
single_obs_tensor = torch.tensor(single_obs_scaled, dtype=torch.float32)

model.eval()  # Put the model in evaluation mode
with torch.no_grad():
    prediction = model(single_obs_tensor)
    print(prediction.item())

"""### Predicting the Test set results"""

X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

with torch.no_grad():
    y_pred = model(X_test_tensor)
    y_pred = y_pred.round()

"""### Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred.numpy())
print(cm)
