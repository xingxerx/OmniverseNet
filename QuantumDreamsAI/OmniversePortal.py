import OmniversePortal 
class QuantumOmniverseDecision(QuantumDecision):
    def __init__(self, *args):
        super().__init__(*args)
        self.omniverse_portal = OmniversePortal()
    def make_decision(self):
        decision = super().make_decision()
        self.omniverse_portal.transition_to_reality(decision)
        return decision
