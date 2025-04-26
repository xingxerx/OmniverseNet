import matplotlib.pyplot as plt
import random

# Simulate Wi-Fi signal strength
wifi_signals = {"Star1": -30, "Star2": -50, "Star3": -70}

# Generate star positions
stars = {name: (random.uniform(-1, 1), random.uniform(-1, 1)) for name in wifi_signals.keys()}

# Plot the stars
plt.figure(figsize=(6, 6))
for name, strength in wifi_signals.items():
    x, y = stars[name]
    brightness = (100 + strength) / 100  # Scale brightness by signal strength
    plt.scatter(x, y, s=100, alpha=brightness, label=name)

plt.title("Holographic Star Map")
plt.legend()
plt.show()