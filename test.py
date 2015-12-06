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

def test_listmatching():
    @listmatching
    def head(lst):
        x, xs = lst[0,]
        return x
    testlist = list(range(5))
    assert head(testlist) == 0
    assert MatchObject(testlist)[0,1] == (0,1,[2,3,4])
    assert MatchObject(testlist)[1,3] == (1,3,[0,2,4])

