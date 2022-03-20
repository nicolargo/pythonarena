#!/usr/bin/env python3

from typing import overload

class Foo(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @overload
    def put(self, name: int) -> int:
        self.name = int(name)
        return self.name

    def put(self, name):
        self.name = name
        return self.name

if __name__ == "__main__":
    foo = Foo("foo")
    print(foo)
    print(type(foo.put("bar")))
    print(type(foo.put(42)))
