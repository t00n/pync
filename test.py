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

def test_patternmatching():
    @patternmatching
    def fibo(n__lt=0):
        raise ValueError("Can not compute fibonacci for negative values !")
    @patternmatching
    def fibo(n__lt=2):
        return 1
    @patternmatching
    def fibo(n):
        return fibo(n-1) + fibo(n-2)
    assert [fibo(i) for i in range(5)] == [1,1,2,3,5]
    with pytest.raises(ValueError):
        fibo(-10)
    @patternmatching
    def a(n__eq=0):
        return 0
    with pytest.raises(ValueError):
        a(1)
    @patternmatching
    def test(a, b, c__lt=0):
        return 0
    @patternmatching
    def test(a, b__eq=1, c__eq=2):
        return 1
    @patternmatching
    def test(a, b__lt=1, c__eq=2):
        return 2
    @patternmatching
    def test(a__le=1, b__gt=2, c__eq=3):
        return 3
    @patternmatching
    def test(a, b, c):
        return 10
    assert test(1,1,-1) == 0
    assert test(1,1,0) == 10
    assert test(1,1,2) == 1
    assert test(1,2,2) == 10
    assert test(1,1,3) == 10
    assert test(1,0,2) == 2
    assert test(1,0,3) == 10
    assert test(1,3,2) == 10
    assert test(1,1,1) == 10
    assert test(0,3,3) == 3

def test_patternmatching_annotations():
    @patternmatching
    def fibo2(n: lambda x: x < 0):
        raise ValueError("Can not compute fibonacci for negative values !")
    @patternmatching
    def fibo2(n: lambda x: x < 2):
        return 1
    @patternmatching
    def fibo2(n):
        return fibo2(n-1) + fibo2(n-2)
    assert [fibo2(i) for i in range(5)] == [1,1,2,3,5]
    with pytest.raises(ValueError):
        fibo2(-10)

def test_patternmatching_BOTH():
    @patternmatching
    def fibo3(n: lambda x: x < 0):
        raise ValueError("Can not compute fibonacci for negative values !")
    @patternmatching
    def fibo3(n__lt=2):
        return 1
    @patternmatching
    def fibo3(n):
        return fibo3(n-1) + fibo3(n-2)
    assert [fibo3(i) for i in range(5)] == [1,1,2,3,5]
    with pytest.raises(ValueError):
        fibo3(-10)


def test_import_hook():
    from _import_hook import importer
    importer.add_matchers('test_module')
    importer.register_importer()
    import test_module
    assert test_module.test_func(1)(5)(3) == 9
    assert test_module.test_func(1,5,3) == 9
    assert test_module.a[0,2] == (0,6,[2,8,7])
    assert test_module.b[1,3,4] == (4,64,49,[0,36])
