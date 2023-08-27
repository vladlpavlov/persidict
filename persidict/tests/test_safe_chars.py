from persidict.safe_chars import replace_unsafe_chars

def test_replace_unsafe_chars():
    assert replace_unsafe_chars("a@b*c", "_") == "a_b_c"
    assert replace_unsafe_chars("X Y&Z", "") == "XYZ"