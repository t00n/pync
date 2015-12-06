from pync import *
import pytest

@curry
def testfunc(x, y):
    return (x, y)

def test_curry():
    assert testfunc(1, 1) == (1,1)
    a = testfunc(1)
    assert a(1) == (1,1)
    assert a(2) == (1,2)
    assert testfunc(2)(2) == (2,2)
    with pytest.raises(TypeError):
        a()
        testfunc()