# e:\OmniverseNet\QEITCodePrototype.py
import numpy as np
# It's better practice to import specific components you need
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
try:
    from qiskit_aer import Aer # For simulators
except ImportError:
    print("ERROR: qiskit-aer is required for simulation. Please install it: pip install qiskit-aer")
    Aer = None # Indicate Aer is unavailable

# --- Function Definitions ---

# Using the second, more complete definition provided in your code
def generate_entangled_pair():
  """Creates a circuit for a 2-qubit Bell state |Φ+>."""
  qr = QuantumRegister(2, name="q") # Give registers names
  cr = ClassicalRegister(2, name="c")
  circuit = QuantumCircuit(qr, cr, name="Entanglement")
  circuit.h(qr[0])
  circuit.cx(qr[0], qr[1])
  return circuit, qr, cr # Return registers

def encode_data(circuit, qr, data): # Accept qr
  """Encodes a classical bit (0 or 1) onto the first qubit (qr[0])."""
  if data == 1:
    circuit.x(qr[0])
  # No need to return circuit, it's modified in-place

# --- Corrected measure_and_decode function ---
def measure_and_decode(circuit, qr, cr, backend, shots=1024): # Accept qr, cr, backend, add shots arg
  """Measures the circuit, runs it on the backend, and decodes the result."""
  circuit.measure(qr, cr)
  print("Circuit before execution:\n", circuit) # Optional: See the circuit

  if backend is None:
      print("Backend not available.")
      return None # Or raise an error

  # --- FIX: Replace execute with backend.run() ---
  job = backend.run(circuit, shots=shots) # Use the run method of the backend
  result = job.result()
  # --- End of Fix ---

  counts = result.get_counts(circuit)
  print("Counts:", counts) # See the results

  # Simple decoding logic (can be refined)
  # Assumes '00' means 0 was sent, '11' means 1 was sent
  count_00 = counts.get('00', 0)
  count_11 = counts.get('11', 0)
  decoded_data = 1 if count_11 > count_00 else 0
  return decoded_data

# --- Main Execution Block ---
if __name__ == "__main__":
    if Aer is None:
        exit(1) # Exit if Aer couldn't be imported

    try:
        backend = Aer.get_backend('qasm_simulator')
    except Exception as e:
        print(f"Error getting Aer backend: {e}")
        exit(1)

    # 1. Generate pair
    entanglement_circuit, qr, cr = generate_entangled_pair()

    # 2. Choose data
    data_to_send = 1 # Or 0

    # 3. Encode (on a copy to keep original separate if needed)
    teleport_circuit = entanglement_circuit.copy(name="Encoding")
    encode_data(teleport_circuit, qr, data_to_send) # Pass qr

    # 4. Measure and Decode
    received_data = measure_and_decode(teleport_circuit, qr, cr, backend) # Pass qr, cr, backend

    if received_data is not None:
        print(f"\nSent data: {data_to_send}")
        print(f"Received data: {received_data}")
        if data_to_send == received_data:
            print("Transmission Successful!")
        else:
            print("Transmission Failed!")

