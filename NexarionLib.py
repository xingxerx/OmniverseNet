import torch # Unused import
import torch.nn as nn # Unused import
import torch.nn.functional as F # Unused import
import numpy as np

class NexarionLib:
    def __init__(self):
        pass

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        # Note: This assumes 'x' is the *output* of sigmoid, not the original input
        # If 'x' is the original input, it should be:
        # s = self.sigmoid(x)
        # return s * (1 - s)
        return x * (1 - x)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def tanh(self, x):
        return np.tanh(x)

    def tanh_derivative(self, x):
        # Note: Similar to sigmoid_derivative, this assumes 'x' is the output of tanh
        # If 'x' is the original input, it should be:
        # t = self.tanh(x)
        # return 1 - t**2
        return 1 - x**2 # Corrected from np.tanh(x)**2 if x is the output

    def softmax(self, x):
        # Numerically stable softmax
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def cross_entropy_loss(self, y_true, y_pred):
        # Assumes y_true is one-hot encoded
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        # Correct calculation for batch
        loss = -np.sum(y_true * np.log(y_pred), axis=-1)
        return np.mean(loss) # Average over the batch

    def mse_loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred)**2)

    def mse_loss_derivative(self, y_true, y_pred):
        # Derivative should be averaged over the batch size as well
        return 2 * (y_pred - y_true) / y_true.shape[0] # Use shape[0] for batch size

    def binary_cross_entropy_loss(self, y_true, y_pred):
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return np.mean(loss) # Average over the batch

    def binary_cross_entropy_loss_derivative(self, y_true, y_pred):
        # Implementation needed
        # Derivative is: (y_pred - y_true) / (y_pred * (1 - y_pred)) / batch_size
        # Need to handle potential division by zero near 0 and 1
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon) # Clip to avoid division by zero
        derivative = (y_pred - y_true) / (y_pred * (1 - y_pred))
        return derivative / y_true.shape[0] # Average over batch size
        # pass # Original

    def categorical_cross_entropy_loss(self, y_true, y_pred):
        # This is actually the same as cross_entropy_loss if y_true is one-hot
        # Let's keep the original cross_entropy_loss for that.
        # If y_true contains class indices, it's different (sparse categorical cross-entropy)
        # Assuming y_true is one-hot encoded like cross_entropy_loss
        return self.cross_entropy_loss(y_true, y_pred)
        # pass # Original

    def categorical_cross_entropy_loss_derivative(self, y_true, y_pred):
        # Implementation needed
        # If y_true is one-hot, the derivative w.r.t. the pre-softmax activations (logits)
        # is simply (y_pred - y_true) / batch_size, where y_pred is the softmax output.
        # This function calculates the derivative w.r.t y_pred (softmax output), which is more complex.
        # Often, the derivative is combined with the softmax derivative for backprop.
        # A common simplification for backprop is (y_pred - y_true) / batch_size
        # Let's assume that's what's needed here for simplicity:
        return (y_pred - y_true) / y_true.shape[0] # Average over batch size
        # pass # Original

# --- This block is now correctly unindented ---
if __name__ == "__main__":
    # This code runs only when the script is executed directly
    lib = NexarionLib()
    print("Testing NexarionLib functions:")

    # --- Test Data ---
    print("\n--- Basic Activation Tests ---")
    data = np.array([[1.0, -2.0, 0.5], [-0.1, 0.9, 2.5]]) # Batch of 2 samples
    print(f"Input data:\n{data}")

    sigmoid_output = lib.sigmoid(data)
    print(f"Sigmoid output:\n{sigmoid_output}")
    # Test sigmoid derivative (assuming input is sigmoid output)
    print(f"Sigmoid derivative (on output):\n{lib.sigmoid_derivative(sigmoid_output)}")


    relu_output = lib.relu(data)
    print(f"ReLU output:\n{relu_output}")
    print(f"ReLU derivative:\n{lib.relu_derivative(data)}") # Derivative depends on original input

    tanh_output = lib.tanh(data)
    print(f"Tanh output:\n{tanh_output}")
    # Test tanh derivative (assuming input is tanh output)
    print(f"Tanh derivative (on output):\n{lib.tanh_derivative(tanh_output)}")

    # --- Softmax and Loss Tests ---
    print("\n--- Softmax and Loss Tests ---")
    logits = np.array([[2.0, 1.0, 0.1], [0.5, 1.5, -0.5]]) # Example pre-softmax outputs (batch size 2)
    y_true_one_hot = np.array([[1, 0, 0], [0, 1, 0]]) # Example one-hot labels

    softmax_output = lib.softmax(logits)
    print(f"Softmax input (logits):\n{logits}")
    print(f"Softmax output (y_pred):\n{softmax_output}")
    print(f"Sum of softmax outputs per sample: {np.sum(softmax_output, axis=-1)}") # Should be close to 1

    ce_loss = lib.cross_entropy_loss(y_true_one_hot, softmax_output)
    print(f"Cross-Entropy Loss: {ce_loss:.4f}")
    ce_loss_deriv = lib.categorical_cross_entropy_loss_derivative(y_true_one_hot, softmax_output)
    print(f"Categorical CE Loss Derivative (y_pred - y_true)/N:\n{ce_loss_deriv}")


    # --- MSE Loss Test ---
    print("\n--- MSE Loss Test ---")
    y_true_reg = np.array([[0.9, 0.1], [0.2, 0.8]]) # Example regression targets
    y_pred_reg = np.array([[0.8, 0.2], [0.3, 0.7]]) # Example regression predictions

    mse = lib.mse_loss(y_true_reg, y_pred_reg)
    print(f"MSE Loss: {mse:.4f}")
    mse_deriv = lib.mse_loss_derivative(y_true_reg, y_pred_reg)
    print(f"MSE Loss Derivative:\n{mse_deriv}")

    # --- Binary Cross-Entropy Test ---
    print("\n--- Binary Cross-Entropy Test ---")
    y_true_bin = np.array([[1], [0], [1], [0]]) # Example binary targets (batch size 4)
    y_pred_bin_logits = np.array([[2.0], [-1.0], [0.5], [-0.1]]) # Example pre-sigmoid logits
    y_pred_bin = lib.sigmoid(y_pred_bin_logits) # Apply sigmoid to get probabilities

    print(f"BCE True Labels:\n{y_true_bin}")
    print(f"BCE Predicted Probabilities:\n{y_pred_bin}")

    bce_loss = lib.binary_cross_entropy_loss(y_true_bin, y_pred_bin)
    print(f"Binary Cross-Entropy Loss: {bce_loss:.4f}")
    bce_deriv = lib.binary_cross_entropy_loss_derivative(y_true_bin, y_pred_bin)
    print(f"Binary CE Loss Derivative:\n{bce_deriv}")

