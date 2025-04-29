# e:\OmniverseNet\QEITCodePrototype.py
import numpy as np
# Consider importing specific items instead of '*' for better clarity and safety
# from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import * # Keeping original import for now, but specific imports are recommended

# --- Function Definitions ---
# (Assuming you are using the second set of definitions in your file,
#  as the line numbers in the error match those)

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
def measure_and_decode(circuit, qr, cr, backend, shots=1024):
  """Measures the circuit, runs it on the backend, and decodes the result."""
  circuit.measure(qr, cr)
  print("Circuit before execution:\n", circuit)

  if backend is None:
      print("Error: Backend object is None. Cannot run the circuit.")
      return None

  job = backend.run(circuit, shots=shots)
  result = job.result()
  counts = result.get_counts(circuit)
  print("Counts:", counts)

  # --- Corrected Decoding Logic ---
  # Get counts for all possible outcomes
  count_00 = counts.get('00', 0)
  count_11 = counts.get('11', 0)
  count_01 = counts.get('01', 0)
  count_10 = counts.get('10', 0)

  # Check if the pair {00, 11} or {01, 10} has more counts
  correlated_counts = count_00 + count_11   # Expected for sending 0
  anti_correlated_counts = count_01 + count_10 # Expected for sending 1

  # Decode based on which pair dominates
  if anti_correlated_counts > correlated_counts:
      decoded_data = 1
      print("Decoded based on dominance of '01'/'10' counts.")
  else:
      decoded_data = 0
      print("Decoded based on dominance of '00'/'11' counts.")
  # --- End of Corrected Logic ---

  # Optional: Refine the warning message
  # if (count_01 > 0 or count_10 > 0) and decoded_data == 0:
  #     print("Warning: Detected '01' or '10' outcomes, but decoded as 0.")
  # elif (count_00 > 0 or count_11 > 0) and decoded_data == 1:
  #      print("Warning: Detected '00' or '11' outcomes, but decoded as 1.")

  return decoded_data


# --- Main Execution Block ---
if __name__ == "__main__":
    backend = None # Initialize backend to None
    try:
        # It's good practice to import specific modules where needed
        from qiskit_aer import Aer
        backend = Aer.get_backend('qasm_simulator')
    except ImportError:
        print("ERROR: qiskit-aer not found or failed to import.")
        print("Please install it: pip install qiskit-aer")
        exit(1) # Exit if backend cannot be initialized
    except Exception as e:
        print(f"An error occurred while getting the backend: {e}")
        exit(1)


    # 1. Generate pair
    entanglement_circuit, qr, cr = generate_entangled_pair()
    print("Generated entanglement circuit.")

    # 2. Choose data
    data_to_send = 1 # Or 0
    print(f"Data to send: {data_to_send}")

    # 3. Encode (on a copy to keep original separate if needed)
    teleport_circuit = entanglement_circuit.copy(name="Encoding")
    encode_data(teleport_circuit, qr, data_to_send) # Pass qr here
    print("Encoded data onto circuit.")

    # 4. Measure and Decode
    print("Measuring and decoding...")
    # Pass shots explicitly if you want something other than the default
    received_data = measure_and_decode(teleport_circuit, qr, cr, backend, shots=2048)

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
        print("\nDecoding failed.")

