import numpy as np
from qiskit import QuantumCircuit, transpile
# Ensure you have qiskit-aer installed: pip install qiskit-aer
try:
    from qiskit_aer import AerSimulator
except ImportError:
    print("Warning: qiskit-aer not found. Please install using 'pip install qiskit-aer'")
    # Fallback or raise error if AerSimulator is critical
    AerSimulator = None # Or define a dummy simulator if needed for basic checks

import math
import warnings

class QuantumDecision:
    """
    A class to simulate a decision-making process using a simplified
    quantum approach based on predefined classical probabilities.

    This implementation uses amplitude encoding to represent the probability
    distribution in a quantum state and simulates its measurement.
    """
    def __init__(self, outcomes, probabilities):
        """
        Initializes the Quantum Decision Maker.

        Args:
            outcomes (list): A list of possible final decision outcomes
                             (can be strings, numbers, etc.).
            probabilities (list): A list of classical probabilities corresponding
                                  to each outcome. Must sum to approximately 1.0.
                                  Must have the same length as outcomes.

        Raises:
            ValueError: If probabilities do not sum to 1, if list lengths
                        mismatch, or if the outcomes list is empty.
            RuntimeError: If qiskit-aer is not installed and simulation is attempted.
        """
        if AerSimulator is None:
             raise RuntimeError("qiskit-aer is required but not installed. Please run 'pip install qiskit-aer'")

        if not math.isclose(sum(probabilities), 1.0, abs_tol=1e-9):
            warnings.warn(f"Probabilities sum to {sum(probabilities)}, which is not exactly 1.0. Normalizing.")
            norm_factor = sum(probabilities)
            if norm_factor <= 0:
                 raise ValueError("Sum of probabilities must be positive for normalization.")
            probabilities = [p / norm_factor for p in probabilities]
            # raise ValueError(f"Probabilities must sum to 1.0. Current sum: {sum(probabilities)}")

        if len(outcomes) != len(probabilities):
            raise ValueError("Outcomes and probabilities lists must have the same length.")
        if len(outcomes) == 0:
            raise ValueError("Outcomes list cannot be empty.")

        self.outcomes = outcomes
        # Store probabilities as numpy array for potential vector operations
        self.probabilities = np.array(probabilities)
        self.num_outcomes = len(outcomes)

        # Determine number of qubits needed to represent outcomes
        # We need 2^n >= num_outcomes
        self.num_qubits = math.ceil(math.log2(self.num_outcomes)) if self.num_outcomes > 0 else 0

    def _calculate_probabilities(self, shots=4096):
        """
        Calculates the probabilities of each outcome using a quantum circuit simulation.
        This implementation uses amplitude encoding based on the input classical probabilities.

        Args:
            shots (int): The number of simulated measurements to perform. Higher
                         numbers give results closer to theoretical probabilities.

        Returns:
            dict: A dictionary mapping each outcome to its simulated probability.
        """
        if self.num_outcomes == 0:
            return {}

        # Calculate the amplitudes (sqrt of probabilities)
        amplitudes = np.sqrt(self.probabilities)

        # Determine the dimension of the Hilbert space for the qubits
        target_dim = 2**self.num_qubits

        # Pad amplitudes with zeros if num_outcomes is not a power of 2
        initial_state = np.zeros(target_dim, dtype=complex)
        initial_state[:self.num_outcomes] = amplitudes

        # --- Quantum Circuit Construction ---
        qc = QuantumCircuit(self.num_qubits, name="decision_qc")
        qc.initialize(initial_state, range(self.num_qubits))
        qc.measure_all()
        # ------------------------------------

        # --- Simulation ---
        simulator = AerSimulator()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(compiled_circuit)
        # -----------------

        # --- Process Results ---
        calculated_probabilities = {}
        total_valid_shots = 0 # Count shots corresponding to defined outcomes

        for i, outcome in enumerate(self.outcomes):
            binary_index = format(i, f'0{self.num_qubits}b')
            qiskit_key = binary_index[::-1] # Reverse for Qiskit's typical ordering
            count = counts.get(qiskit_key, 0)
            calculated_probabilities[outcome] = count
            total_valid_shots += count

        if total_valid_shots > 0:
             for outcome in calculated_probabilities:
                 calculated_probabilities[outcome] /= total_valid_shots
        # ---------------------

        return calculated_probabilities

    def make_decision(self, sample=True, shots=4096):
        """
        Makes a decision based on the calculated quantum probabilities.
        """
        quantum_probabilities_dict = self._calculate_probabilities(shots=shots)

        if not quantum_probabilities_dict:
             return None if sample else {}

        if sample:
            outcome_list = list(quantum_probabilities_dict.keys())
            prob_list = np.array(list(quantum_probabilities_dict.values()))
            prob_list /= prob_list.sum() # Ensure normalization for np.random.choice
            chosen_outcome = np.random.choice(outcome_list, p=prob_list)
            return chosen_outcome
        else:
            return quantum_probabilities_dict

    def __str__(self):
        """Provides a string representation of the QuantumDecision object."""
        return (f"QuantumDecision(num_outcomes={self.num_outcomes}, "
                f"num_qubits={self.num_qubits}, "
                f"outcomes={self.outcomes}, "
                f"probabilities={self.probabilities.tolist()})")