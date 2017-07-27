#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# url -H "Content-Type: application/json" -X POST -d '{"key1": 1, "key2": 2}' http://localhost:6789
#

from bottle import run, request, post


@post('/')
def index():
    postdata = request.body.read()
    print(postdata)
    return postdata


run(host='localhost', port=6789, debug=True)
