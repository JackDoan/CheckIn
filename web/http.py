#!/usr/bin/env python
from flask import Flask, render_template, request, Response
import sqlite3, time
from functools import wraps
import libcheckinweb
chn = libcheckinweb


def status_color(status):
	if status[0] == 'T':
		status = btnyellow + status
	elif status[0] == 'P':
		status = btngreen + status
	elif status[0] == 'O':
		status = btnblue + status
	return status

def get_config():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select * from config;")
	config = db.fetchall()
	conn.close()
	classblocks = []
	for pair in config:
		if pair[0] == "class_blocks":
			blocks = str(pair[1]).split()
			for block in blocks:
				block_start = block + "_start"
				block_end = block + "_end"
				for each in config:
					if each[0] == block_start:
						block_start_time = each[1]
					if each[0] == block_end:
						block_end_time = each[1]
				classblocks.append([block, int(block_start_time), int(block_end_time)])
	return classblocks

def check_auth(username, password):
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

btnblue = '<button type="button" class="btn btn-primary btn-xs">'
btngreen = '<button type="button" class="btn btn-success btn-xs">'
btnyellow = '<button type="button" class="btn btn-warning btn-xs">'

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/records')
@requires_auth
def data():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from records order by rowid desc")
	records = map(list, db.fetchall())
	classblocks = get_config()
	for r in records[:]:
		db.execute("Select name from students where rowid=?", (r[1],))
		r[1] = str(db.fetchone()[0])
		if r[4] == "Test":
			classtime = int(time.strftime('%H%M', time.localtime(r[3]))) 
			if classtime > int(classblocks[0][1] - 48) and classtime < classblocks[0][1]: #TODO: -8 accounts for 1st grace period
				status = "Present for " + classblocks[0][0]
			elif classtime > classblocks[0][2] and classtime < classblocks[1][1]:
				status = "Present for " + classblocks[1][0]
			elif classtime > classblocks[1][2] and classtime < classblocks[2][1]:
				status = "Present for " + classblocks[2][0]
			elif classtime > classblocks[2][2] and classtime < classblocks[3][1]:
				status = "Present for " + classblocks[3][0]
			elif classtime > classblocks[3][2] and classtime < classblocks[4][1]:
				status = "Present for " + classblocks[4][0]
			elif classtime > classblocks[0][1] and classtime < classblocks[0][2]:
			#	tardyby = str(classtime - classblocks[0][1])
			#	tardyby = '{:0>4}'.format(tardyby)				####TODO? add tardyby times
			#	tardyby = tardyby[0] + tardyby[1] + ':' + tardyby[2] + tardyby[3]
				status = 'Tardy for ' + classblocks[0][0]
			elif classtime > classblocks[1][1] and classtime < classblocks[1][2]:
				status = 'Tardy for ' + classblocks[1][0]
			elif classtime > classblocks[2][1] and classtime < classblocks[2][2]:
				status = 'Tardy for ' + classblocks[2][0]
			elif classtime > classblocks[3][1] and classtime < classblocks[3][2]:
				status = 'Tardy for ' + classblocks[3][0]
			elif classtime > classblocks[4][1] and classtime < classblocks[4][2]:
				status = 'Tardy for ' + classblocks[4][0]
			else:
				status = 'OOB: record at ' + str(classtime)

			db.execute('update records set status=? where rowid=?', (status, r[0]))
			r[4] = status_color(status)
		else:
			#	records.remove(r)	removes OOB errors from display -- commented out for testing.
			r[4] = status_color(r[4])

		r[3] = chn.epochToString(r[3])
	conn.commit()
	conn.close()
	return render_template('data.html', records=records)

@app.route('/student/<student_id>')
@requires_auth
def newstudentPage(student_id):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	s = chn.Student(student_id)
	db.execute("Select rowid,* from records where `student_id`=? order by rowid desc", (student_id,))
	records = map(list, db.fetchall())
	for r in records:
		r[3] = chn.epochToString(r[3])
		r[4] = status_color(r[4])
	classblocks = get_config()
	classlist = []
	for block in classblocks:
		db.execute("Select * from classes where timeblock = ?", (block[0],))
		result = map(list, db.fetchall())
		classlist.append(result)
	conn.close()
	return render_template('student.html', currentclasses=s.classes, classblocks=classblocks, classlist=classlist, records=records, student_id = student_id, tag=s.tag, name=s.name)

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

@app.route('/students')
@requires_auth
def tags():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	students = map(list, db.fetchall())
	conn.close()
	newid = students[-1][0]+1
	return render_template('tags.html', students=students, newid=newid)

@app.route('/students/add')
@requires_auth
def tagsadd():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	students = map(list, db.fetchall())
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


@app.route('/students/delete', methods=['GET', 'POST'])
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

@app.route('/students/edit', methods=['GET', 'POST'])
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

@app.route('/class', methods=['GET', 'POST'])
def classes_list():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select * from classes")
	classes = db.fetchall()
	conn.close()
	return render_template('classes.html', classes=classes)

@app.route('/debug', methods=['GET', 'POST'])
def le_debug():
	raise
	return 'Ohnoes'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

