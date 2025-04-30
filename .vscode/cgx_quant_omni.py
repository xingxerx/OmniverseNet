import multiverse_core as mc
from quantum_gateways import QuantumGateway
from entanglement_protocol import EntanglementProtocol
# Initialize Multiverse Core
mc.init()
# Create Quantum Gateway
gateway = QuantumGateway(mc)
# Establish Entanglement Protocol
protocol = EntanglementProtocol(gateway