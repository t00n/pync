""" This file is heavily inspired by Pyrthon.
    Original : https://github.com/tobgu/pyrthon/blob/master/pyrthon/_import_hook.py

    Copyright (c) 2015 Tobias Gustafsson

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
"""

import imp
import os
import types
import sys
from redbaron import RedBaron
from pync import *

def functionalize(src):
    red = RedBaron(src)
    red.insert(0, 'import pync')
    for func in red.find_all('def'):
        func.decorators.append('@pync.curry')

    for l in red.find_all('list') + red.find_all('list_comprehension'):
        l.replace("pync.list(%s)" % l)

    return red.dumps()

class PyncImporter(object):
    def __init__(self):
        self._match_expressions = []

    def register_importer(self):
        sys.meta_path.insert(0, self)

    def module_matches(self, name):
        for expr in self._match_expressions:
            if callable(expr):
                if expr(name):
                    return True

            else:
                if expr.endswith('*') and name.startswith(expr[:-1]):
                    return True

                if expr == name:
                    return True

        return False

    def add_matchers(self, *matchers):
        self._match_expressions.extend(matchers)

    def find_module(self, name, path=None):
        if self.module_matches(name):
            return self

        return None

    def load_module(self, name):
        try:
            suffix = name.split('.')[-1]
            fd, pathname, (suffix, mode, type_) = imp.find_module(suffix)
        except ImportError:
            return None

        module = types.ModuleType(name) #create empty module object

        with fd:
            if type_ == imp.PY_SOURCE:
                filename = pathname
            elif type_ == imp.PY_COMPILED:
                filename = pathname[:-1]
            elif type_ == imp.PKG_DIRECTORY:
                filename = os.path.join(pathname, '__init__.py')
                module.__path__ = [pathname]
            else:
                return imp.load_module(name, fd, pathname, (suffix, mode, type_))

            if filename != pathname:
                try:
                    with open(filename, 'U') as real_file:
                        src = real_file.read()
                except IOError: #fallback
                    return imp.load_module(name, fd, pathname, (suffix, mode, type_))
            else:
                src = fd.read()

        module.__file__ = filename
        inlined = functionalize(src)
        code = compile(inlined, filename, 'exec')
        sys.modules[name] = module
        exec(code,  module.__dict__)

        return module

importer = PyncImporter()


