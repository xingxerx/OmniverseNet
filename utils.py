# In E:\OmniverseNet\utils.py

# Instead of this at the top:
# from OmniverseNet import some_config_value

def some_utility_function():
    # Import only when the function is called
    from OmniverseNet import some_config_value
    # Now use some_config_value
    print(f"Using config: {some_config_value}")
    # ... rest of function ...
