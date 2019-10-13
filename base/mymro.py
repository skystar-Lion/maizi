#!/usr/bin/env python
# -*- coding=utf-8 -*-

import inspect

class o:
    pass

class e(o):
    pass

class f(o):
    pass

class d(o):
    pass
class b(d, e):
    pass

class c(d, f):
    pass

class a(b, c):
    pass

if __name__ == '__main__':
    print(inspect.getmro(a))