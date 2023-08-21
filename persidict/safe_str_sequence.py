import string
from collections.abc import Sequence
from typing import Tuple

SAFE_CHARS_SET = set(string.ascii_letters + string.digits + "()_-~.=")


class SafeStrSequence(Sequence):
    """A sequence of non-emtpy URL/filename-safe strings.
    """

    safe_strings: Tuple[str, ...]

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SafeStrSequence):
            self.safe_strings = args[0].safe_strings
        else:
            candidate = []
            for a in args:
                assert isinstance(a, str)
                assert len(a) > 0
                assert len(set(a) - SAFE_CHARS_SET) == 0
                candidate.append(a)
            self.safe_strings = tuple(candidate)

    def __getitem__(self, key):
        return self.safe_strings[key]

    def __len__(self):
        return len(self.safe_strings)

    def __repr__(self):
        return f"SafeStrSequence({self.safe_strings})"

    # def __str__(self):
    #     return self.__repr__()

    def __eq__(self, other):
        assert isinstance(other, SafeStrSequence)
        return self.safe_strings == other.safe_strings

    def __add__(self, other):
        other = SafeStrSequence(other)
        return SafeStrSequence(*(self.safe_strings + other.safe_strings))

    def __radd__(self, other):
        other = SafeStrSequence(other)
        return SafeStrSequence(*(other.safe_strings + self.safe_strings))

    def __iter__(self):
        return iter(self.safe_strings)

    def __contains__(self, item):
        return item in self.safe_strings

    def __reversed__(self):
        return SafeStrSequence(*reversed(self.safe_strings))