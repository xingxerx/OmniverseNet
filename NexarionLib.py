import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class NexarionLib:
    def __init__(self):
        pass

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def tanh(self, x):
        return np.tanh(x)

    def tanh_derivative(self, x):
        return 1 - np.tanh(x)**2

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def cross_entropy_loss(self, y_true, y_pred):
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.sum(y_true * np.log(y_pred))
        return loss / float(y_true.shape[0])

    def mse_loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred)**2)

    def mse_loss_derivative(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / y_true.size

    def binary_cross_entropy_loss(self, y_true, y_pred):
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss

    def binary_cross_entropy_loss_derivative(self):
        pass

    def categorical_cross_entropy_loss(self):
        pass

    def categorical_cross_entropy_loss_derivative(self):
        pass 