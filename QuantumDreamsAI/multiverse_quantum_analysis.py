import pandas as pd
import numpy as np

# Import the function to generate data dynamically
from multiverse_ingestion import ingest_multiverse_data
from qiskit import QuantumCircuit, transpile

# Import the Aer simulator from qiskit_aer
try:
    from qiskit_aer import AerSimulator
except ImportError:
    print("Please install qiskit-aer: pip install qiskit-aer")
    exit()

# Generate multiverse data instead of loading from CSV
print("Generating multiverse data...")
df = ingest_multiverse_data() # Use default parameters or specify as needed
print(f"Generated {len(df)} data points.")
# Convert data to qubit inputs (0/1)
df['Data'] = np.where(df['Data'] > 0.5, 1, 0)
# Create quantum circuit
def create_quantum_circuit(data):
    qc = QuantumCircuit(1)
    if data == 1:
        qc.x(0)  # Apply X gate for |1⟩ state
    qc.h(0)  # Apply H gate for superposition
    return qc

# Initialize the simulator once outside the loop for efficiency
simulator = AerSimulator()

# Apply quantum gates to data
quantum_data = []
print("\nStarting quantum simulations...")
try:
    for index, row in df.iterrows():
        try:
            qc = create_quantum_circuit(row['Data'])
            # Add measurement - required for getting counts from simulator
            qc.measure_all()
            # Compile the circuit for the simulator
            compiled_circuit = transpile(qc, simulator)
            # Run the simulation using simulator.run()
            result = simulator.run(compiled_circuit, shots=1).result()
            counts = result.get_counts(compiled_circuit)
            quantum_data.append([row['Universe'], row['Reality'], list(counts.keys())[0]])
        except Exception as e:
            print(f"Error during simulation for row {index} (Universe: {row.get('Universe', 'N/A')}, Reality: {row.get('Reality', 'N/A')}): {e}")
            # Decide if you want to continue or stop on error
            # continue # Uncomment to skip problematic rows
            # break    # Uncomment to stop the loop on the first error
except Exception as loop_error:
    print(f"\nAn unexpected error occurred outside the inner simulation loop: {loop_error}")
    # Optionally re-raise the error if you want the script to stop completely
    # raise loop_error
# Save quantum results
print("\n--- Preparing to save quantum results ---")
quantum_df = pd.DataFrame(quantum_data, columns=['Universe', 'Reality', 'Quantum_State'])
print("Columns in DataFrame before saving:")
print(quantum_df.columns)
print("First 5 rows of DataFrame before saving:")
print(quantum_df.head())
print("-" * 30)
quantum_df.to_csv('multiverse_quantum_results.csv', index=False)
print("Quantum analysis complete. Results saved to multiverse_quantum_results.csv")
