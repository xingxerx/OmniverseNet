import datetime

class BattleLogger:
    """A simple class to manage and store battle log entries."""

    def __init__(self):
        """Initializes an empty battle log."""
        self.log_entries = []

    def log_event(self, description: str):
        """Adds a new event to the battle log with a timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {description}"
        self.log_entries.append(entry)
        print(entry) # Optional: print the event as it happens

    def get_log(self) -> list[str]:
        """Returns the entire list of log entries."""
        return self.log_entries

    def display_log(self):
        """Prints the entire battle log to the console."""
        print("\n--- Battle Log ---")
        if not self.log_entries:
            print("The log is empty.")
        else:
            for entry in self.log_entries:
                print(entry)
        print("--- End Log ---")

# --- Example Usage ---
if __name__ == "__main__":
    battle_log = BattleLogger()

    battle_log.log_event("Battle started between Hero and Goblin!")
    battle_log.log_event("Hero attacks Goblin for 15 damage.")
    battle_log.log_event("Goblin misses Hero.")
    battle_log.log_event("Hero uses Fireball, dealing 30 damage to Goblin.")
    battle_log.log_event("Goblin defeated!")
    battle_log.log_event("Battle ended.")

    # Display the full log at the end
    battle_log.display_log()

    # You can also get the raw list of entries
    # full_log_list = battle_log.get_log()
    # print("\nRaw log list:", full_log_list)
