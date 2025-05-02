
import re

def is_valid_email(email: str) -> bool:
    """
    Validate if the given string is a valid email address.

    This function checks if the input string conforms to a basic email format:
    - Contains exactly one '@' symbol
    - Has at least one character before the '@'
    - Has at least one character between '@' and '.'
    - Has at least two characters after the last '.'
    - Contains only alphanumeric characters, dots, hyphens, and underscores

    Args:
    email (str): The string to be validated as an email address

    Returns:
    bool: True if the input is a valid email address, False otherwise

    Examples:
    >>> is_valid_email("user@example.com")
    True
    >>> is_valid_email("invalid.email@com")
    False
    >>> is_valid_email("@invalid.com")
    False
    """
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

if __name__ == "__main__":
    import doctest
    doctest.testmod() # This will run the tests in the docstring
    # Example usage with invalid email
    print(is_valid_email("invalid.email@com"))