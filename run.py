from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for

__author__ = 'martin'

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 5001
app = Flask(__name__)
app.secret_key = 'development key'







if __name__ == '__main__':
    app.run(SERVER_NAME, SERVER_PORT, debug=True, threaded=True)


