import numpy as np
from qiskit import *
def generate_entangled_pair():
  qr = QuantumRegister(2)
  cr = ClassicalRegister(2)
  circuit = QuantumCircuit(qr, cr)
  circuit.h(qr[0])
  circuit.cx(qr[0], qr[1])
  return circuit
def encode_data(circuit, data):
  if data == 1:
    circuit.x(qr[0])
  return circuit
def measure_and_decode(circuit):
  circuit.measure(qr, cr)
  job = execute(circuit, backend)
  result = job.result()
  counts = result.get_counts(circuit)
  decoded_data = 1 if counts['11'] > counts['00'] else 0
  return decoded_data

