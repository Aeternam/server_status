from bottle import Bottle, run
from bottle import template


app = Bottle()
@app.route('/hello')
def hello():
    return "Hello world!"

@app.route('/')
@app.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

#@route('/wiki/<pagename>')
#def show_wiki_page(pagename):

@route('/object/<id:int>')
def callback(id):
	assert isinstance(id, int)

@route('/show/<name:re:[a-z]+>')
def callback(name):
	assert name.isalpha()

@route('/static/<path:path>')
def callback(path):
	return static_file(path,...)	

run(app, host='0.0.0.0', port=8080, debug=True)
