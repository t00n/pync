from functools import wraps, partial
from inspect import signature

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
    def wrapper(*args, **kwargs):
        return Function(func)(*args, **kwargs)
    return wrapper

class List(list):
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            lst = [self[i] for i in key]
            lst.append([x for i, x in enumerate(self) if i not in key])
            return tuple(lst)
        return super(List, self).__getitem__(key)
