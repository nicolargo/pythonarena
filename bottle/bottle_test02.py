from bottle import route, run, template

@route('/hello')
def hello():
    return template('bottle_test02', name='World')

run(host='localhost', port=8080, debug=True)