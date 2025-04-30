# e:\OmniverseNet\NexarionLib.py

# Remove these lines:
# import torch # Unused import
# import torch.nn as nn # Unused import
# import torch.nn.functional as F # Unused import

import numpy as np # Keep this one

class NexarionLib:
    """A library for various mathematical and utility functions."""
    def __init__(self):
        pass # Constructor currently does nothing

    def sigmoid(self, x):
        """Calculates the sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    # ... rest of the class ...

# --- This block is now correctly unindented ---
if __name__ == "__main__":
    # Example usage/testing code can go here
    lib = NexarionLib()
    test_data = np.array([-2, -1, 0, 1, 2])
    sigmoid_result = lib.sigmoid(test_data)
    print(f"Input data: {test_data}")
    print(f"Sigmoid output: {sigmoid_result}")
    pass
