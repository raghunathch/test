
from bottle import Bottle, run, static_file, template, error

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/magic')
def magic():
    return "Magic! 2 routes!!"

@app.route('/go')
def magic():
    return static_file('htm_test.htm' , root='/Users/Raghunath/pythonpractice')

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.error(404)
def error404(error):
    return 'Nothing here, sorry'

run(app, host='localhost', port=8080)