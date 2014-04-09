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

@app.route('/student/<student>')
@requires_auth
def studentPage(student):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students where `name`=?", (student,))
	result = db.fetchall()
	if result:
		tag = result[0][2]
		student_id = result[0][0]
	else:
		conn.close()
		tags()
	db.execute("Select rowid,* from records where `student_id`=? order by rowid desc", (student_id,))
	t_records = db.fetchall()
	records = map(list, t_records)
	i = 0
	for r in records:
		#comptime = time.strftime('%H%M', time.localtime(r[3])
		#if comptime 
		r[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r[3]))

	conn.close()
	return render_template('student.html', records=records, student_id = student_id, tag=tag, name=student)

@app.route('/student/<student>/edit')
@requires_auth
def studentEdit(student):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	if request.args.getlist('tag'):
		name = student
		tag = request.args.getlist('tag')[0]
		db.execute("Update `students` set `tag`=? WHERE `name`=?;", (tag, name,))
	conn.commit()
	return studentPage(student)	


@app.route('/tags')
@requires_auth
def tags():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
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
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	t_students = db.fetchall()
	students = map(list, t_students)
	newid = students[-1][0]+1
	if request.args.getlist('name') and request.args.getlist('tag'):
		newstudent = request.args.getlist('name')[0]
		newtag = request.args.getlist('tag')[0]
		db.execute("INSERT INTO `students` (`name`, `tag`) VALUES (?, ?);", (newstudent, newtag,))
		students.append([newid, newstudent, newtag])
		conn.commit()
		newid = students[-1][0]+1 #needed to increment on screen!
		conn.close()
		return render_template('tags.html', students=students, newid=newid)
	else:
		conn.close()
		return render_template('tags.html', students=students, newid=newid)


@app.route('/tags/delete', methods=['GET', 'POST'])
def tagsdel():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	if request.args.getlist('delid'):
		delid = request.args.getlist('delid')[0]
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
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	if request.args.getlist('name') and request.args.getlist('tag'):
		name = request.args.getlist('name')[0]
		tag = request.args.getlist('tag')[0]
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

