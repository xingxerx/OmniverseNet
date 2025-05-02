import pandas as pd
from cross_reality_analytics import identify_optimal_realities
# Import the class definition, not inside the method
from reality_transition_gateway import RealityTransitionGateway
class OmniversalDecisionEngine:
    def __init__(self, cross_reality_analysis):
        self.cross_reality_analysis = cross_reality_analysis
        self.optimal_realities = identify_optimal_realities(cross_reality_analysis)
    def make_decision(self):
        # Select top reality based on predicted stability score
        top_reality = self.optimal_realities.iloc[0]
        
        # Create decision output
        decision_output = {
            'Selected Reality': top_reality.name,
            'Predicted Stability': top_reality['Predicted Stability']
        }
        
        return decision_output
    def activate_reality_transition(self, decision_output, gateway):
        # Activate reality transition to selected reality
        gateway.transition_to_reality(decision_output['Selected Reality'])
def activate_engine(cross_reality_analysis, gateway):
    engine = OmniversalDecisionEngine(cross_reality_analysis)
    decision_output = engine.make_decision()
    engine.activate_reality_transition(decision_output, gateway)
    print("Omniversal decision made and reality transition activated!")
