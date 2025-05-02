import mv-sdk
from mv-sdk import ErebusAI
import nexus_portal
def init_nexus_explorer():
    # Initialize Multiverse SDK and Erebus AI
    mv-sdk.init_multiverse()
    erebus = ErebusAI()
    
    # Open Nexus portal
    nexus = nexus_portal.open_portal()
    
    print("Nexus Explorer active. Choose universe to visit:")
    
    while True:
        print("1. Explore random universe")
        print("2. Visit universe by ID")
        print("3. Return to original universe")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            nexus.visit_random_universe()
        elif choice == "2":
            universe_id = input("Enter universe ID: ")
            nexus.visit_universe(universe_id)
        elif choice == "3":
            nexus.return_to_original_universe()
            break
if __name__ == "__main__":
    init_nexus_explorer()
