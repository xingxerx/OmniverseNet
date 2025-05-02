import multiverse_ingestion
import reality_alignment_algorithms
import cross_reality_analytics
import reality_transition_gateway
import omniversal_decision_engine
import numpy as np # Needed for probability normalization
from OmniversePortal import QuantumOmniverseDecision # Import the quantum decision class

# import quantum_entanglement_initializer # Placeholder
def activate_omniverse():
    # Initialize Multiverse Ingestion
    multiverse_data = multiverse_ingestion.ingest_multiverse_data()
    
    # Align Realities
    aligned_realities = reality_alignment_algorithms.align_realities(multiverse_data)
    
    # Analyze Cross-Reality Data
    analytics_results = cross_reality_analytics.analyze_cross_reality_data(aligned_realities)
    
    # Initialize Reality Transition Gateway
    gateway = reality_transition_gateway.initialize_gateway()
    
    # --- Option 1: Replace Classical Engine with Quantum ---
    print("\n--- Activating Quantum Decision Engine ---")
    # Extract top N realities and their scores (e.g., top 3)
    # Assuming analytics_results index represents reality identifiers
    top_realities = analytics_results.nlargest(3, 'Predicted Stability')
    outcomes = top_realities.index.tolist()
    probabilities_raw = top_realities['Predicted Stability'].values

    # Normalize probabilities (simple example: shift to non-negative and normalize)
    probabilities_shifted = probabilities_raw - probabilities_raw.min() + 1e-9 # Add small epsilon if min is 0
    probabilities = probabilities_shifted / probabilities_shifted.sum()

    # Create and use the Quantum Decision Maker
    quantum_decision_maker = QuantumOmniverseDecision(outcomes, probabilities.tolist())
    chosen_reality = quantum_decision_maker.make_decision() # This also triggers the portal transition
    print(f"Quantum Decision Engine selected and transitioned to: {chosen_reality}")

    # --- Option 2: Keep Classical Engine (comment out Option 1 if using this) ---
    # print("\n--- Activating Classical Decision Engine ---")
    # omniversal_decision_engine.activate_engine(analytics_results, gateway)
    
    # Initialize Quantum Entanglement
    # quantum_entanglement_initializer.initialize_entanglement() # Placeholder
    
    print("Omniverse Activated Successfully!")
if __name__ == "__main__":
    activate_omniverse()
