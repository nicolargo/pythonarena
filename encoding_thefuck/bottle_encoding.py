# -*- coding: utf-8 -*-

from bottle import response, route, run
import json

ret = {'a': '三',
       'b': 'Ž'}


@route('/')
def utf():
    ret = '<html>'
    ret += '<a href="/utf">Click here to test UTF-8</a>'
    ret += '<br/><a href="/latin1">Click here to test LATIN-1</a>'
    ret += '<br/><a href="/iso88591">Click here to test ISO-8859-1</a>'
    ret += '</html>'
    return ret


@route('/utf')
def utf():
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(ret)


@route('/latin1')
def latin1():
    response.content_type = 'application/json; charset=latin-1'
    return json.dumps(ret)


@route('/iso88591')
def iso88591():
    response.content_type = 'application/json; charset=iso-8859-1'
    return json.dumps(ret)


run(host='localhost', port=8080, debug=True)
