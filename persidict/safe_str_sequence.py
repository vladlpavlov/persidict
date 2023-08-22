import base64
import hashlib
import string
from collections.abc import Sequence
from typing import Tuple, Any

SAFE_CHARS_SET = set(string.ascii_letters + string.digits + "()_-~.=")

def _is_sequence(obj:Any)->bool:
    """Check if obj is a sequence."""
    if isinstance(obj, Sequence):
        return True
    elif (hasattr(obj, "__getitem__") and callable(obj.__getitem__)
        and hasattr(obj, "__len__") and callable(obj.__len__)
        and hasattr(obj, "__iter__") and callable(obj.__iter__)):
        return True
    else:
        return False

class SafeStrSequence(Sequence):
    """A sequence of non-emtpy URL/filename-safe strings.
    """

    safe_strings: Tuple[str, ...]

    def __init__(self, *args):
        candidate = []
        for a in args:
            if isinstance(a, SafeStrSequence):
                candidate.extend(a.safe_strings)
            elif isinstance(a, str):
                assert len(a) > 0
                assert len(set(a) - SAFE_CHARS_SET) == 0
                candidate.append(a)
            elif _is_sequence(a):
                candidate.extend(SafeStrSequence(*a).safe_strings)
            else:
                assert False, f"Invalid argument type: {type(a)}"
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



def _create_signature_suffix(input_str:str, digest_len:int) -> str:
    """ Create a hash signature suffix for a string."""

    assert isinstance(input_str, str)

    if digest_len == 0:
        return ""

    input_b = input_str.encode()
    hash_object = hashlib.md5(input_b)
    full_digest_str = base64.b32encode(hash_object.digest()).decode()
    suffix = "_" + full_digest_str[:digest_len]

    return suffix


def _add_signature_suffix_if_absent(input_str:str, digest_len:int) -> str:
    """ Add a hash signature suffix to a string if it's not there."""

    assert isinstance(input_str, str)

    if digest_len == 0:
        return input_str

    if len(input_str) > digest_len + 1:
        possibly_already_present_suffix = _create_signature_suffix(
            input_str[:-1-digest_len], digest_len)
        if input_str.endswith(possibly_already_present_suffix):
            return input_str

    return input_str + _create_signature_suffix(input_str, digest_len)


def _add_all_suffixes_if_absent(
        str_seq:SafeStrSequence
        ,digest_len:int
        ) -> SafeStrSequence:
    """Add hash signature suffixes to all strings in a SafeStrSequence."""

    str_seq = SafeStrSequence(str_seq)

    new_seq = []
    for s in str_seq:
        new_seq.append(_add_signature_suffix_if_absent(s,digest_len))

    new_seq = SafeStrSequence(*new_seq)

    return new_seq

def _remove_signature_suffix_if_present(input_str:str, digest_len:int) -> str:
    """ Remove a hash signature suffix from a string if it's detected."""

    assert isinstance(input_str, str)

    if digest_len == 0:
        return input_str

    if len(input_str) > digest_len + 1:
        possibly_already_present_suffix = _create_signature_suffix(
            input_str[:-1-digest_len], digest_len)
        if input_str.endswith(possibly_already_present_suffix):
            return input_str[:-1-digest_len]

    return input_str

def _remove_all_signature_suffixes_if_present(
        str_seq:SafeStrSequence
        , digest_len:int
        ) -> SafeStrSequence:
    """Remove hash signature suffixes from all strings in a SafeStrSequence."""

    str_seq = SafeStrSequence(str_seq)

    if digest_len == 0:
        return str_seq

    new_seq = []
    for s in str_seq:
        new_string = _remove_signature_suffix_if_present(s, digest_len)
        new_seq.append(new_string)

    new_seq = SafeStrSequence(*new_seq)

    return new_seq

def sign_safe_str_sequence(str_seq:SafeStrSequence
                           , digest_len:int
                           ) -> SafeStrSequence:
    """Add hash signature suffixes to all strings in a SafeStrSequence."""

    str_seq = SafeStrSequence(str_seq)

    str_seq = _add_all_suffixes_if_absent(str_seq, digest_len)

    return str_seq

def unsign_safe_str_sequence(str_seq:SafeStrSequence
                             , digest_len:int
                             ) -> SafeStrSequence:
    """Remove hash signature suffixes from all strings in a SafeStrSequence."""

    str_seq = SafeStrSequence(str_seq)

    str_seq = _remove_all_signature_suffixes_if_present(str_seq, digest_len)

    return str_seq
