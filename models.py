# Example technique (apply this logic in your data.py if applicable)
# Instead of importing at the top:
# from OmniverseNet import some_needed_item

def function_that_needs_item():
    # Import only when needed inside the function
    from OmniverseNet import some_needed_item
    # Now use some_needed_item
    result = some_needed_item.do_something()
    # ...
