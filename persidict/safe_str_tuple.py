import string
from collections.abc import Sequence, Mapping, Hashable
from typing import Tuple, Any

SAFE_CHARS_SET = set(string.ascii_letters + string.digits + "()_-~.=")

def _is_sequence_not_mapping(obj:Any)->bool:
    """Check if obj is a sequence."""
    if isinstance(obj, Sequence) and not isinstance(obj, Mapping):
        return True
    elif (hasattr(obj, "__getitem__") and callable(obj.__getitem__)
        and hasattr(obj, "__len__") and callable(obj.__len__)
        and hasattr(obj, "__iter__") and callable(obj.__iter__)
        and not isinstance(obj, Mapping)):
        return True
    else:
        return False

class SafeStrTuple(Sequence, Hashable):
    """A sequence of non-emtpy URL/filename-safe strings.
    """

    the_strings: Tuple[str, ...]

    def __init__(self, *args):
        assert len(args) > 0
        candidate = []
        for a in args:
            if isinstance(a, SafeStrTuple):
                candidate.extend(a.the_strings)
            elif isinstance(a, str):
                assert len(a) > 0
                assert len(set(a) - SAFE_CHARS_SET) == 0
                candidate.append(a)
            elif _is_sequence_not_mapping(a):
                if len(a) > 0:
                    candidate.extend(SafeStrTuple(*a).the_strings)
            else:
                assert False, f"Invalid argument type: {type(a)}"
        self.the_strings = tuple(candidate)

    def __getitem__(self, key):
        return self.the_strings[key]

    def __len__(self):
        return len(self.the_strings)

    def __hash__(self):
        return hash(self.the_strings)

    @classmethod
    def allowed_characters(cls):
        return SAFE_CHARS_SET

    def __repr__(self):
        return f"SafeStrSequence({self.the_strings})"


    def __eq__(self, other):
        assert isinstance(other, SafeStrTuple)
        return self.the_strings == other.the_strings


    def __add__(self, other):
        other = SafeStrTuple(other)
        return SafeStrTuple(*(self.the_strings + other.the_strings))

    def __radd__(self, other):
        other = SafeStrTuple(other)
        return SafeStrTuple(*(other.the_strings + self.the_strings))

    def __iter__(self):
        return iter(self.the_strings)

    def __contains__(self, item):
        return item in self.the_strings

    def __reversed__(self):
        return SafeStrTuple(*reversed(self.the_strings))