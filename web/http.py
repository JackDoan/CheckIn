#!/usr/bin/env python
from flask import Flask, render_template, request, Response
import sqlite3, time
from functools import wraps

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
def data():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	#db.execute("Select * from config")
	#config = db.fetchall()
	db.execute("Select rowid,* from records order by rowid desc")
	t_records = db.fetchall()
	records = map(list, t_records)
	i = 0
	for r in records:
		db.execute("Select name from students where rowid=?", (r[1],))
		r[1] = str(db.fetchone()[0])
		#comptime = time.strftime('%H%M', time.localtime(r[3])
		#if comptime 
		r[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r[3]))

	conn.close()
	return render_template('data.html', records=records)

@app.route('/tags')
@requires_auth
def tags():
	conn = sqlite3.connect("../chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	t_students = db.fetchall()
	students = map(list, t_students)
	conn.close()
	newid = students[-1][0]+1
	return render_template('tags.html', students=students, newid=newid)

@app.route('/tags/add')
@requires_auth
def tagsadd():
	conn = sqlite3.connect("../chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	t_students = db.fetchall()
	students = map(list, t_students)
	newstudent = request.args.getlist('name')[0]
	newtag = request.args.getlist('tag')[0]
	newid = students[-1][0]+1
	db.execute("INSERT INTO `students` (`name`, `tag`) VALUES (?, ?);", (newstudent, newtag,))
	students.append([newid, newstudent, newtag])
	conn.commit()
	newid = students[-1][0]+1 #needed to increment on screen!
	if request.args.getlist('crash'):
			raise
			return "oh shit"
	conn.close()
	return render_template('tags.html', students=students, newid=newid, query_ok=1, printstatus=1, newstudent=newstudent, newtag=newtag)


@app.route('/tags/delete', methods=['GET', 'POST'])
def tagsdel():
	conn = sqlite3.connect("../chn.db")
	delid = request.args.getlist('delid')[0]
	db = conn.cursor()
	db.execute("DELETE FROM `records` WHERE `student_id`=?;", (delid,))
	db.execute("DELETE FROM `students` WHERE `rowid`=?;", (delid,))
	db.execute("Select rowid,* from students")
	students = db.fetchall()
	conn.commit()
	conn.close()
	newid = students[-1][0]+1
	return render_template('tags.html', newid=newid, students=students)

@app.route('/tags/edit', methods=['GET', 'POST'])
def tagsedit():
	conn = sqlite3.connect("../chn.db")
	name = request.args.getlist('name')[0]
	tag = request.args.getlist('tag')[0]
	db = conn.cursor()
	db.execute("Update `students` set `tag`=? WHERE `name`=?;", (tag, name,))
	db.execute("Select rowid,* from students")
	students = db.fetchall()
	conn.commit()
	conn.close()
	newid = students[-1][0]+1
	return render_template('tags.html', newid=newid, students=students)

@app.route('/debug', methods=['GET', 'POST'])
def le_debug():
	raise
	return 'Ohnoes'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

