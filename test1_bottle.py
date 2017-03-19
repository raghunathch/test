from bottle import get, post, request, Bottle, run # or route


@get('/login') # or @route('/login')
def login():
    return '''
        <center>
        <form action="/login" method="post"><br><br>
            <br><br>Please enter your credentials to access the portal <br><br>
            Username: <input name="username" type="text" /><br>
            Password: <input name="password" type="password" /><br>
            <input value="Reset Form" type="reset">
            <input value="Login" type="submit" />
        </form>
        <button type="button">Forgot Password</button>
        <button type="button">Sign Up</button>
        </center>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"


def check_login(username, password):
    if username == "raghunath" and password == "password":
        return True
    else:
        return False

run(host='localhost', port=8080, debug=True)
