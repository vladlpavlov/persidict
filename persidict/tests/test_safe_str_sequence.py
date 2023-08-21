from persidict import SafeStrSequence

def test_add():
    l1 = ['a', 'b', 'c']
    l2 = ['d', 'e', 'f']
    s1 = SafeStrSequence(*l1)
    s2 = SafeStrSequence(*l2)
    assert s1 + s2 == SafeStrSequence(*l1, *l2)
    assert s2 + s1 == SafeStrSequence(*l2, *l1)

def test_radd():
    l1 = ['a', 'b', 'c']
    l2 = ['d', 'e', 'f']
    s1 = SafeStrSequence(*l1)
    s2 = SafeStrSequence(*l2)
    assert s1 + s2 == SafeStrSequence(*l1, *l2)
    assert s2 + s1 == SafeStrSequence(*l2, *l1)

def test_eq():
    l1 = ['a', 'b', 'c']
    l2 = ['d', 'e', 'f']
    s1 = SafeStrSequence(*l1)
    s2 = SafeStrSequence(*l2)
    assert s1 == SafeStrSequence(*l1)
    assert s2 == SafeStrSequence(*l2)
    assert s1 != s2

def test_getitem():
    l = ['a', 'b', 'c', 'd', 'e', 'x', 'y', 'z']
    s = SafeStrSequence(*l)
    for i, c in enumerate(s):
        assert s[i] == l[i] == c
    assert s == SafeStrSequence(s)

def test_len():
    l = ['a', 'b', 'c']
    s = SafeStrSequence(*l)
    assert len(s) == len(l)

def test_contains():
    l = ['a', 'b', 'c']
    s = SafeStrSequence(*l)
    for c in l:
        assert c in s
        assert c*10 not in s

def test_reversed():
    l = ['a', 'b', 'c', 'x', 'y', 'z']
    s = SafeStrSequence(*l)
    assert s == reversed(reversed(s))
    assert s != reversed(s)

def test_count():
    l = ['a', 'b', 'c', 'a']
    s = SafeStrSequence(*l)
    for c in l:
        assert s.count(c) == l.count(c)
        assert s.count(c*100) == 0

def test_init():
    l = ['a', 'b', 'c']
    s = SafeStrSequence(*l)
    assert s == SafeStrSequence(s)
    assert s == SafeStrSequence(*l)
    assert s != reversed(s)
    assert s != SafeStrSequence(*l, 'd')
    assert s != SafeStrSequence(*l, 'd', 'e')
    assert s != SafeStrSequence(*l, 'd', 'e', 'f')
