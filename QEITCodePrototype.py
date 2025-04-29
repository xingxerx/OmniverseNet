# e:\OmniverseNet\QEITCodePrototype.py
import numpy as np
# 1. Specific Imports
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.providers.backend import BackendV1 as Backend # For type hinting backend
from qiskit.result import Result
from qiskit.qobj.utils import MeasLevel

# Type hinting imports
from typing import Tuple, Optional, Dict

# --- Constants ---
DEFAULT_SHOTS = 2048

# --- Function Definitions ---

def generate_entangled_pair() -> Tuple[QuantumCircuit, QuantumRegister, ClassicalRegister]:
  """Creates a circuit for a 2-qubit Bell state |Φ+>."""
  qr = QuantumRegister(2, name="q")
  cr = ClassicalRegister(2, name="c")
  circuit = QuantumCircuit(qr, cr, name="Entanglement")
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

def measure_and_decode(
    circuit: QuantumCircuit,
    qr: QuantumRegister,
    cr: ClassicalRegister,
    backend: Backend, # Use imported Backend type
    shots: int = DEFAULT_SHOTS
) -> Optional[int]:
  """Measures the circuit, runs it on the backend, and decodes the result."""
  circuit.measure(qr, cr)
  print("Circuit before execution:\n", circuit)

  if backend is None:
      print("Error: Backend object is None. Cannot run the circuit.")
      return None

  try:
      # Use backend.run() - ensure backend is compatible or use execute if needed
      # Note: backend.run() might return different job types depending on provider
      job = backend.run(circuit, shots=shots)
      result: Result = job.result() # Add type hint for result
      counts: Dict[str, int] = result.get_counts(circuit)
      print("Counts:", counts)
  except Exception as e:
      print(f"Error running/getting results from backend: {e}")
      return None


  # --- Corrected Decoding Logic ---
  count_00 = counts.get('00', 0)
  count_11 = counts.get('11', 0)
  count_01 = counts.get('01', 0)
  count_10 = counts.get('10', 0)

  correlated_counts = count_00 + count_11   # Expected for sending 0
  anti_correlated_counts = count_01 + count_10 # Expected for sending 1

  if anti_correlated_counts > correlated_counts:
      decoded_data = 1
      print("Decoded based on dominance of '01'/'10' counts.")
  else:
      # Default to 0 if counts are equal or correlated counts dominate
      decoded_data = 0
      print("Decoded based on dominance of '00'/'11' counts (or tie).")

  # Optional: Add warning for unexpected states if significant
  total_counts = sum(counts.values())
  unexpected_counts = total_counts - correlated_counts - anti_correlated_counts
  if unexpected_counts > 0:
      print(f"Warning: Detected {unexpected_counts}/{total_counts} counts in unexpected states.")

  return decoded_data


# --- Main Execution Block ---
if __name__ == "__main__":
    backend_instance: Optional[Backend] = None # Type hint for backend
    try:
        from qiskit_aer import Aer
        # Specify the desired simulator
        backend_instance = Aer.get_backend('qasm_simulator')
        print(f"Using backend: {backend_instance.name}")
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
    print("Generated entanglement circuit.")

    # 2. Choose data
    data_to_send: int = 1 # Or 0
    print(f"Data to send: {data_to_send}")

    # 3. Encode
    teleport_circuit = entanglement_circuit.copy(name="Encoding")
    encode_data(teleport_circuit, qr, data_to_send)
    print("Encoded data onto circuit.")

    # 4. Measure and Decode
    print("Measuring and decoding...")
    received_data: Optional[int] = measure_and_decode(
        teleport_circuit, qr, cr, backend_instance, shots=DEFAULT_SHOTS
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

