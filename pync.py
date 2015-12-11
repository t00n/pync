from functools import wraps, partial
from inspect import signature, _empty
from copy import copy
from collections import Callable

class Function():
    def __init__(self, function):
        self.function = function
        self.args = []
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        if len(self.args) + len(self.kwargs) >= len(signature(self.function).parameters):
            return self.function(*self.args, **self.kwargs)
        else:
            return self

def curry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Function(func)(*args, **kwargs)
    return wrapper

class List(list):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            lst = [self[i] for i in key]
            lst.append([x for i, x in enumerate(self) if i not in key])
            return tuple(lst)
        return super(List, self).__getitem__(key)

functions = {}

def _patternmatching(parameters, annotations, *args, **kwargs):
    ok, i = True, 0
    for arg, param in parameters.items():
        if param.default != _empty and param.name[-4:] in ["__eq", "__ne", "__lt", "__le", "__gt", "__ge"]:
            if not eval('args[i].%s__(param.default)' % param.name[-4:] ):
                ok = False
        if arg in annotations and isinstance(annotations[arg], Callable) and not annotations[arg](args[i]):
            ok = False
        i+=1
    return ok

def patternmatching(func):
    key = func.__name__
    if key not in functions:
        functions[key] = []
    functions[key].append(copy(func))
    @wraps(func)
    def wrapper(*args, **kwargs):
        for function in functions[key]:
            sign = signature(function)
            if _patternmatching(sign.parameters, function.__annotations__, *args, **kwargs):
                return function(*args, **kwargs)
        raise ValueError("No pattern for %s with args : " % func.__name__, args, kwargs)
    return wrapper