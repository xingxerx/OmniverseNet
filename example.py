import matplotlib.pyplot as plt
import numpy as np
import random

def generate_hologram():
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Quantum entanglement qubits
    qubit_positions = np.random.rand(10, 3) * 10  # Random positions for 10 qubits
    for i, pos in enumerate(qubit_positions):
        ax.scatter(*pos, s=100, color="blue", label=f"Qubit {i+1}" if i == 0 else "")  # Label only the first

    # Entanglement lines
    for i in range(len(qubit_positions) - 1):
        ax.plot([qubit_positions[i][0], qubit_positions[i + 1][0]],
                [qubit_positions[i][1], qubit_positions[i + 1][1]],
                [qubit_positions[i][2], qubit_positions[i + 1][2]], color="cyan", alpha=0.6)

    # Stars based on Wi-Fi data (signal strength simulates brightness)
    wifi_signals = {"Star1": -40, "Star2": -60, "Star3": -80}
    for name, signal_strength in wifi_signals.items():
        star_position = np.random.rand(3) * 10
        brightness = (100 + signal_strength) / 100  # Brightness scales with signal
        ax.scatter(*star_position, s=100 * brightness, color="yellow", label=name)

    ax.set_title("Holographic Quantum Entanglement & Star Map", fontsize=16)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    generate_hologram()