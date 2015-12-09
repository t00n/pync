from pync import *
import pytest

def test_curry():
    @curry
    def testfunc(x, y, z):
        return x + y + z
    assert testfunc(1, 1, 1) == 3
    assert testfunc(1,1)(1) == 3
    assert testfunc(1)(1,1) == 3
    assert testfunc(1)(1)(1) == 3
    with pytest.raises(TypeError):
        testfunc(1,1,1,1)
    with pytest.raises(TypeError):
        testfunc(1,1,1)(1)
    with pytest.raises(TypeError):
        testfunc(1,1)(1,1)

def test_listmatching():
    @listmatching
    def head(lst):
        x, xs = lst[0,]
        return x
    testlist = list(range(5))
    assert head(testlist) == 0
    assert MatchObject(testlist)[0,1] == (0,1,[2,3,4])
    assert MatchObject(testlist)[1,3] == (1,3,[0,2,4])


def test_import_hook():
    from _import_hook import importer
    importer.register_modules('test_module')
    importer.register_importer()
    import test_module
    assert test_module.test_func(1)(5)(3) == 9
    assert test_module.test_func(1,5,3) == 9
