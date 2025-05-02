import numpy as np
from qiskit import QuantumCircuit, transpile
# Ensure you have qiskit-aer installed: pip install qiskit-aer
from qiskit_aer import AerSimulator
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
        """
        if not math.isclose(sum(probabilities), 1.0, abs_tol=1e-9):
            warnings.warn(f"Probabilities sum to {sum(probabilities)}, which is not exactly 1.0. Normalizing.")
            norm_factor = sum(probabilities)
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

        # Initialize the state using amplitude encoding
        # Qiskit's initialize prepares the state |psi> = sum(a_i |i>)
        qc.initialize(initial_state, range(self.num_qubits))

        # Add measurements to classical bits (required for qasm_simulator/real hardware)
        qc.measure_all()
        # ------------------------------------

        # --- Simulation ---
        # Use AerSimulator for efficient simulation
        simulator = AerSimulator()

        # Compile the circuit for the simulator backend for optimization
        compiled_circuit = transpile(qc, simulator)

        # Run the simulation
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(compiled_circuit)
        # -----------------

        # --- Process Results ---
        calculated_probabilities = {}
        total_valid_shots = 0 # Count shots corresponding to defined outcomes

        for i, outcome in enumerate(self.outcomes):
            # Format the index as a binary string matching qubit count
            binary_index = format(i, f'0{self.num_qubits}b')
            # Qiskit's counts often have reversed qubit order compared to initialize
            # e.g., |q1 q0>, initialize [a,b,c,d] maps to a|00>, b|01>, c|10>, d|11>
            # counts keys might be '00', '10', '01', '11' (reversed)
            qiskit_key = binary_index[::-1]
            count = counts.get(qiskit_key, 0)
            calculated_probabilities[outcome] = count
            total_valid_shots += count

        # Normalize probabilities based on shots that landed in valid outcome states
        if total_valid_shots > 0:
             for outcome in calculated_probabilities:
                 calculated_probabilities[outcome] /= total_valid_shots
        # If total_valid_shots is 0 (highly unlikely unless shots=0 or error), probabilities remain 0
        # ---------------------

        return calculated_probabilities

    def make_decision(self, sample=True, shots=4096):
        """
        Makes a decision based on the calculated quantum probabilities.

        Args:
            sample (bool): If True (default), samples one outcome based on the
                           simulated probabilities.
                           If False, returns the full dictionary of outcomes
                           and their simulated probabilities.
            shots (int): Number of shots for the simulation used to determine
                         the probability distribution for sampling or returning.

        Returns:
            - If sample is True: The chosen outcome (type depends on input outcomes).
            - If sample is False: A dictionary mapping each outcome to its
                                  simulated probability.
        """
        quantum_probabilities_dict = self._calculate_probabilities(shots=shots)

        if not quantum_probabilities_dict: # Handle empty case
             return None if sample else {}

        if sample:
            # Sample an outcome based on the calculated quantum probabilities
            outcome_list = list(quantum_probabilities_dict.keys())
            prob_list = list(quantum_probabilities_dict.values())

            # Ensure probabilities sum to 1 for numpy choice, handle potential float issues
            prob_sum = sum(prob_list)
            if not math.isclose(prob_sum, 1.0, abs_tol=1e-9):
                # This might happen due to simulation noise or if total_valid_shots was 0
                warnings.warn(f"Probabilities for sampling sum to {prob_sum}. Renormalizing.")
                if prob_sum <= 0: # Cannot sample if sum is not positive
                    # Fallback: return the first outcome or handle error appropriately
                    return outcome_list[0] if outcome_list else None
                prob_list = np.array(prob_list) / prob_sum

            chosen_outcome = np.random.choice(outcome_list, p=prob_list)
            return chosen_outcome
        else:
            # Return the full probability distribution calculated
            return quantum_probabilities_dict

    def __str__(self):
        """Provides a string representation of the QuantumDecision object."""
        return (f"QuantumDecision(num_outcomes={self.num_outcomes}, "
                f"num_qubits={self.num_qubits}, "
                f"outcomes={self.outcomes}, "
                f"probabilities={self.probabilities.tolist()})")

# --- Example Usage ---
if __name__ == "__main__":
    possible_outcomes = ["Action A", "Action B", "Action C", "Action D"]
    classical_probs = [0.1, 0.4, 0.3, 0.2] # Must sum to 1.0

    try:
        decision_maker = QuantumDecision(possible_outcomes, classical_probs)
        print("Initialized Decision Maker:")
        print(decision_maker)
        print("-" * 30)

        # Get the simulated probability distribution
        print("Simulated Probabilities (from Qiskit):")
        simulated_probs = decision_maker.make_decision(sample=False, shots=8192)
        for outcome, prob in simulated_probs.items():
            print(f"  - {outcome}: {prob:.4f}")
        print("-" * 30)

        # Make a sampled decision
        print("Making 10 sampled decisions:")
        for i in range(10):
            chosen = decision_maker.make_decision(sample=True, shots=1024)
            print(f"  Decision {i+1}: {chosen}")
        print("-" * 30)

        # Example with outcomes not a power of 2
        outcomes_3 = ["Stay", "Switch", "Fold"]
        probs_3 = [0.5, 0.3, 0.2]
        decision_maker_3 = QuantumDecision(outcomes_3, probs_3)
        print("\nInitialized Decision Maker (3 outcomes):")
        print(decision_maker_3)
        sim_probs_3 = decision_maker_3.make_decision(sample=False, shots=8192)
        print("Simulated Probabilities (3 outcomes):")
        for outcome, prob in sim_probs_3.items():
            print(f"  - {outcome}: {prob:.4f}")
        chosen_3 = decision_maker_3.make_decision(sample=True)
        print(f"Sampled Decision (3 outcomes): {chosen_3}")


    except ValueError as e:
        print(f"Error initializing QuantumDecision: {e}")
    except ImportError:
        print("Error: Qiskit or Qiskit Aer might not be installed.")
        print("Please install using: pip install qiskit qiskit-aer numpy")

