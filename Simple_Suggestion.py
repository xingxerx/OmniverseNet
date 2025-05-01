def get_suggestions(category):
  """Returns a list of suggestions based on the category."""
  if category == "fruit":
    return ["apple", "banana", "orange"]
  elif category == "color":
    return ["red", "green", "blue"]
  else:
    return ["suggestion1", "suggestion2"] # Default suggestions

# Example usage:
# print(get_suggestions("fruit"))
# print(get_suggestions("other"))