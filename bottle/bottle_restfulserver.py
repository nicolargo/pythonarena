#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# curl -H "Content-Type: application/json" -X POST -d '{"key1": 1, "key2": 2}' http://localhost:6789/post
#

from bottle import run, request, post, route, response
import zlib
import json
import struct
import time

data = {'my': 'json'}


@post('/post')
def api_post():
    global data
    data = json.loads(request.body.read())
    return(data)


@route('/get')
def api_get():
    global data
    response.headers['Content-Encoding'] = 'identity'
    return(json.dumps(data).encode('utf-8'))


@route('/getgzip')
def api_get_gzip():
    global data
    ret = json.dumps(data).encode('utf-8')
    if 'gzip' in request.headers.get('Accept-Encoding', ''):
        response.headers['Content-Encoding'] = 'gzip'
        ret = gzip_body(ret)
    else:
        response.headers['Content-Encoding'] = 'identity'
    return(ret)


def write_gzip_header():
    header = '\037\213'      # magic header
    header += '\010'         # compression method
    header += '\0'
    header += struct.pack("<L", long(time.time()))
    header += '\002'
    header += '\377'
    return header


def write_gzip_trailer(crc, size):
    footer = struct.pack("<l", crc)
    footer += struct.pack("<L", size & 0xFFFFFFFFL)
    return footer


def gzip_body(body, compress_level=6):
    # Compress page
    yield write_gzip_header()
    crc = zlib.crc32("")
    size = 0
    zobj = zlib.compressobj(compress_level,
                            zlib.DEFLATED, -zlib.MAX_WBITS,
                            zlib.DEF_MEM_LEVEL, 0)
    for line in body:
        size += len(line)
        crc = zlib.crc32(line, crc)
        yield zobj.compress(line)
    yield zobj.flush()
    yield write_gzip_trailer(crc, size)


run(host='localhost', port=6789, debug=True)
