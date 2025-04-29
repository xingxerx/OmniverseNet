# e:\OmniverseNet\QEITCodePrototype.py
import numpy as np
# 1. Specific Imports
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.providers.backend import BackendV1 as Backend # For type hinting backend
from qiskit.result import Result
# REMOVED: from qiskit.qobj.utils import MeasLevel (Not used)

# Type hinting imports
from typing import Tuple, Optional, Dict

# --- Constants ---
DEFAULT_SHOTS = 2048

# --- Function Definitions ---

def generate_entangled_pair() -> Tuple[QuantumCircuit, QuantumRegister, ClassicalRegister]:
  """Creates a circuit for a 2-qubit Bell state |Φ+>."""
  qr = QuantumRegister(2, name="q")
  cr = ClassicalRegister(2, name="c") # Keep classical register for potential measurement later
  circuit = QuantumCircuit(qr, cr, name="Entanglement") # Include cr even if not measured immediately
  circuit.h(qr[0])
  circuit.cx(qr[0], qr[1])
  return circuit, qr, cr

def encode_data(circuit: QuantumCircuit, qr: QuantumRegister, data: int) -> None:
  """Encodes a classical bit (0 or 1) onto the first qubit (qr[0]).
     Modifies the circuit in-place.
  """
  if not isinstance(data, int) or data not in [0, 1]:
      raise ValueError("Data to encode must be 0 or 1.")
  if data == 1:
    circuit.x(qr[0])

# --- NEW: Function to get statevector ---
def get_statevector(
    circuit: QuantumCircuit,
    statevector_backend: Backend # Expecting a statevector simulator backend
) -> Optional[np.ndarray]:
    """Runs the circuit on the statevector simulator and returns the statevector."""
    if statevector_backend is None:
        print("Error: Statevector backend object is None.")
        return None
    # IMPORTANT: Create a copy *without* measurement for statevector simulation
    circuit_copy = circuit.copy()
    # Remove any measurements if they exist on the copy (optional, good practice)
    circuit_copy.remove_final_measurements(inplace=True)

    print("\nCircuit for Statevector Simulation (no measurement):\n", circuit_copy)

    try:
        job = statevector_backend.run(circuit_copy)
        result = job.result()
        statevector = result.get_statevector(circuit_copy)
        print("Statevector obtained successfully.")
        return statevector
    except Exception as e:
        print(f"Error running/getting statevector from backend: {e}")
        return None
# --- End NEW Function ---


def measure_and_decode(
    circuit: QuantumCircuit,
    qr: QuantumRegister,
    cr: ClassicalRegister,
    backend: Backend, # Use imported Backend type
    shots: int = DEFAULT_SHOTS
) -> Optional[int]:
  """Measures the circuit, runs it on the backend, and decodes the result."""
  # --- Measurement instruction triggers collapse simulation ---
  circuit.measure(qr, cr)
  # ---------------------------------------------------------
  print("\nCircuit with Measurement (for qasm_simulator):\n", circuit)

  if backend is None:
      print("Error: Measurement Backend object is None. Cannot run the circuit.")
      return None

  try:
      job = backend.run(circuit, shots=shots)
      result: Result = job.result()
      counts: Dict[str, int] = result.get_counts(circuit)
      # --- Counts show the *results* after simulated collapse ---
      print("\nCounts (Post-Collapse Outcomes):", counts)
      # -------------------------------------------------------
  except Exception as e:
      print(f"Error running/getting results from backend: {e}")
      return None

  # --- Decoding Logic (as before) ---
  count_00 = counts.get('00', 0)
  count_11 = counts.get('11', 0)
  count_01 = counts.get('01', 0)
  count_10 = counts.get('10', 0)

  # Corrected logic based on standard Quantum Teleportation expected states
  # If data=0 sent -> expect |Φ+> -> '00' or '11'
  # If data=1 sent -> X on q0 -> |Ψ+> -> '01' or '10'
  correlated_counts = count_00 + count_11   # Expected for sending 0
  anti_correlated_counts = count_01 + count_10 # Expected for sending 1

  if anti_correlated_counts > correlated_counts:
      decoded_data = 1
      print("Decoded as 1 (dominance of '01'/'10')")
  else:
      # Default to 0 if counts are equal or correlated counts dominate
      decoded_data = 0
      print("Decoded as 0 (dominance of '00'/'11' or tie)")

  total_counts = sum(counts.values())
  # Check for noise/errors (though less likely in ideal simulation)
  # In this simple Bell state prep + optional X gate, we only expect these 4 states.
  # unexpected_counts = total_counts - correlated_counts - anti_correlated_counts
  # if unexpected_counts > 0:
  #     print(f"Warning: Detected {unexpected_counts}/{total_counts} counts in unexpected states.")

  return decoded_data


# --- Main Execution Block ---
if __name__ == "__main__":
    qasm_backend: Optional[Backend] = None
    statevector_backend: Optional[Backend] = None
    try:
        from qiskit_aer import Aer
        # Get both simulators
        qasm_backend = Aer.get_backend('qasm_simulator')
        statevector_backend = Aer.get_backend('statevector_simulator')
        print(f"Using QASM backend: {qasm_backend.name}")
        print(f"Using Statevector backend: {statevector_backend.name}")
    except ImportError:
        print("ERROR: qiskit-aer not found or failed to import.")
        print("Please install it: pip install qiskit-aer")
        exit(1)
    except Exception as e:
        print(f"An error occurred while getting the backend: {e}")
        exit(1)

    # --- Simulation ---
    # 1. Generate pair
    entanglement_circuit, qr, cr = generate_entangled_pair()
    print("\nGenerated entanglement circuit.")

    # 2. Choose data
    data_to_send: int = 1 # Try 0 or 1
    print(f"Data to send: {data_to_send}")

    # 3. Encode
    # Create a base circuit with encoding *before* getting statevector or measuring
    teleport_circuit_base = entanglement_circuit.copy(name="Encoding")
    encode_data(teleport_circuit_base, qr, data_to_send)
    print("Encoded data onto base circuit.")

    # 4. Get Statevector *Before* Collapse
    print("\n--- Inspecting Statevector (Pre-Collapse) ---")
    statevector = get_statevector(teleport_circuit_base, statevector_backend)
    if statevector is not None:
        print("Statevector |psi> = ")
        # Nicer printing for statevector
        basis = [format(i, f'0{qr.size}b') for i in range(2**qr.size)]
        for i, amp in enumerate(statevector):
            if not np.isclose(amp, 0): # Only print non-zero amplitudes
                print(f"  {amp:.3f} |{basis[i]}>")
        # Expected states:
        # data=0 -> |Φ+> = 1/sqrt(2)|00> + 1/sqrt(2)|11> -> [0.707, 0, 0, 0.707]
        # data=1 -> |Ψ+> = 1/sqrt(2)|01> + 1/sqrt(2)|10> -> [0, 0.707, 0.707, 0]

    # 5. Measure and Decode (Simulates Collapse)
    print("\n--- Measuring and Decoding (Simulating Collapse) ---")
    # Use a fresh copy for measurement to ensure measure is added correctly
    measure_circuit = teleport_circuit_base.copy(name="Measurement")
    received_data: Optional[int] = measure_and_decode(
        measure_circuit, qr, cr, qasm_backend, shots=DEFAULT_SHOTS
    )

    # --- Output Results ---
    if received_data is not None:
        print("\n--- Results ---")
        print(f"Sent data:     {data_to_send}")
        print(f"Received data: {received_data}")
        if data_to_send == received_data:
            print("Transmission Successful!")
        else:
            print("Transmission Failed!")
    else:
        print("\nDecoding failed or simulation error occurred.")

