#!/usr/bin/env python
from flask import Flask
from flask import render_template
import sqlite3, time

from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/data')
@requires_auth
def hello_world():
	conn = sqlite3.connect("../chn.db")
        db = conn.cursor()
        db.execute("Select rowid,* from records order by rowid desc")
        t_records = db.fetchall()
	records = map(list, t_records)
	i = 0
	for r in records:
	  db.execute("Select name from students where rowid=?", (r[1],))
	  r[1] = str(db.fetchone()[0])
	  r[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r[3]))
        conn.close()
        return render_template('data.html', records=records)
@app.route('/test')
def test1():
	conn = sqlite3.connect("../datt.db")
	db = conn.cursor()
	db.execute("Select * from students")
	studentnames = db.fetchall()
	conn.close()
	return render_template('test.html', studentnames=studentnames)

if __name__ == '__main__':
	app.debug = True
	app.run()

