"""
Nexus Explorer Application
Uses the Multiverse SDK and Nexus Portal to navigate simulated universes.
"""

import mv_sdk         # Import the SDK module
import nexus_portal   # Import the portal module

def init_nexus_explorer():
    """Initializes and runs the Nexus Explorer interface."""
    # Initialize Multiverse SDK and Erebus AI
    mv_sdk.init_multiverse()
    erebus = mv_sdk.ErebusAI() # Use the class from the imported module

    # Open Nexus portal
    nexus = nexus_portal.open_portal()

    print("Nexus Explorer active. Choose universe to visit:")

    while True:
        print("\n--- Nexus Menu ---")
        print("1. Explore random universe")
        print("2. Visit universe by ID")
        print("3. Return to original universe")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            nexus.visit_random_universe()
        elif choice == "2":
            universe_id = input("Enter universe ID: ")
            nexus.visit_universe(universe_id)
        elif choice == "3":
            nexus.return_to_original_universe()
            print("Returned to original universe. Exiting Nexus Explorer.")
            break
        elif choice == "4":
            print("Exiting Nexus Explorer.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Starting Nexus Explorer...")
    init_nexus_explorer()
    print("Nexus Explorer finished.")