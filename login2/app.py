from flask import Flask, request
from db import init_users_table, create_user
from utilities import setup_logger, get_hash

app = Flask(__name__)

def init():
    init_users_table()
    setup_logger()

init()

@app.route("/")
def hello_world():
    html = """
        <h1>Login:</h1>
        <form action='/login' method='POST'>
            <input type='text' placeholder='username'></input>
            <input type='password' placeholder='password'></input>
            <button>login</button>
        </form>
        <button>sign up</button>
    """
    return html


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # login(username, password)
    return 'WIP'

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    # hash password
    password_hash = get_hash(password)
    if password_hash != None:
        # store user
        create_user(username, password_hash)
        return f'User {username} created'
    else:
        return 'Something went wrong with user creation. Please try again later.'
