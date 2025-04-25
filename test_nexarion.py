# test_nexarion.py
import numpy as np
from NexarionLib import NexarionLib

# Create an instance
lib = NexarionLib()

# Example usage
data = np.array([1.0, -2.0, 0.5])
sigmoid_output = lib.sigmoid(data)
print("Sigmoid:", sigmoid_output)

relu_output = lib.relu(data)
print("ReLU:", relu_output)

# ... test other methods ...
