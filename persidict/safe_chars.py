import string
from copy import deepcopy

SAFE_CHARS_SET = set(string.ascii_letters + string.digits + "()_-~.=")

def get_safe_chars():
    """Return a set of allowed characters."""
    return deepcopy(SAFE_CHARS_SET)
