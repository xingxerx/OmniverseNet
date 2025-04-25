# Instead of this at the top:
# from OmniverseNet import some_utility

class CoreRunner:
    def run(self):
        # Import only when needed
        from OmniverseNet import some_utility
        utility = some_utility()
        # ... rest of the method ...
