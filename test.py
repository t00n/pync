from pync import *
import pytest

def test_curry():
    @curry
    def testfunc(x, y, z):
        return x + y + z
    class testclass():
        @curry
        def testmethod(self, x,y,z):
            return x+y+z
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
    assert testclass().testmethod(1,1,2) == 4
    assert testclass().testmethod(1,1)(2) == 4
    assert testclass().testmethod(1)(1,2) == 4
    assert testclass().testmethod(1)(1)(2) == 4
    with pytest.raises(TypeError):
        testclass().testmethod(1,1,1,1)
    with pytest.raises(TypeError):
        testclass().testmethod(1,1,1)(1)
    with pytest.raises(TypeError):
        testclass().testmethod(1,1)(1,1)

def test_listmatching():
    testlist = List([6,2,1,8,6])
    assert testlist[0,1] == (6,2,[1,8,6])
    assert testlist[1,3] == (2,8,[6,1,6])


def test_import_hook():
    from _import_hook import importer
    importer.register_modules('test_module')
    importer.register_importer()
    import test_module
    assert test_module.test_func(1)(5)(3) == 9
    assert test_module.test_func(1,5,3) == 9
    assert test_module.a[0,2] == (0,6,[2,8,7])
    assert test_module.b[1,3,4] == (4,64,49,[0,36])
