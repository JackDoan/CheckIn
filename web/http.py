#!/usr/bin/env python
from flask import Flask, render_template, request, Response
import sqlite3, time
from functools import wraps
import libcheckinweb, libschedule, libstudent
chn = libcheckinweb

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
		#if not auth or True :#not chn.check_auth(auth.username, auth.password):
			#	return authenticate()
		#	return True
		return f(*args, **kwargs)
	return decorated

app = Flask(__name__)

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/records')
@requires_auth
def records_page():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	records = libstudent.attendance_records()
	db.execute("select COUNT(status) from records")
	totalrecords = int(db.fetchall()[0][0])
	db.execute("select COUNT(status) from records where status LIKE 'Tardy%';")
	tardies = int(db.fetchall()[0][0])
	tardyRatio = [totalrecords, tardies, 100-((float(tardies)/totalrecords)*100)]
	conn.close()
	return render_template('data.html', records=records, tardyRatio=tardyRatio)

@app.route('/student/<student_id>')
@requires_auth
def student_page_detailed(student_id):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	s = chn.Student(student_id)
	db.execute("Select rowid,* from records where `student_id`=? order by rowid desc", (student_id,))
	records = map(list, db.fetchall())
	for r in records:
		r[3] = chn.epochToString(r[3])
		r[4] = chn.status_color(r[4])
	classblocks = chn.get_config()
	classlist = []
	for block in classblocks:
		db.execute("Select * from classes where timeblock = ?", (block[0],))
		result = map(list, db.fetchall())
		classlist.append(result)
	#db.execute("Select COUNT(*) from students")
	db.execute("select COUNT(status) from records where student_id=?", (student_id,))
	totalrecords = int(db.fetchall()[0][0])
	db.execute("select COUNT(status) from records where student_id=? and status LIKE 'Tardy%';", (student_id,))
	tardies = int(db.fetchall()[0][0])
	tardyRatio = [totalrecords, tardies, 100-((float(tardies)/totalrecords)*100)]
	conn.close()
	return render_template('student.html', currentclasses=s.classes, classblocks=classblocks, classlist=classlist, records=records, student_id = student_id, tag=s.tag, name=s.name, tardyRatio=tardyRatio)

@app.route('/student/<student_id>/edit')
@requires_auth
def student_edit_page_detailed(student_id):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	if request.args.getlist('edited'):
		gets = request.args.getlist
		###UGLY HACK FOR PRESENTATION
		class1 = gets('School-schedule')[0]
		class2 = gets('After-School-schedule')[0]
		db.execute("Update `students` set `classes`=? WHERE `rowid`=?;", (str(class1 + ',' + class2), student_id,))
	conn.commit()
	return student_page_detailed(student_id)	

@app.route('/students')
@requires_auth
def student_list_page():
	student = libstudent.student_list()
	return render_template('tags.html', students=student[0], newid=student[1])

@app.route('/students/add')
@requires_auth
def student_add_page():
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
def students_edit_page():
	if request.args.getlist('id') and request.args.getlist('tag'):
		sid = request.args.getlist('id')[0]
		tag = request.args.getlist('tag')[0]
		student = libstudent.student_edit(sid, tag)
	return render_template('tags.html', newid=student[0], students=student[1])

@app.route('/classes', methods=['GET', 'POST'])
@app.route('/class', methods=['GET', 'POST'])
def classes_list_page():
	classes = libschedule.classes_list()
	return render_template('classes.html', classes=classes)

@app.route('/classes/edit', methods=['GET', 'POST'])
def classes_edit_page():
	gets = request.args.getlist
	if gets('classname') and gets('teacher') and gets('time') and gets('loc') and gets('slots') and gets('id'):
		conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
		db = conn.cursor()
		classname = request.args.getlist('classname')[0]
		teacher = request.args.getlist('teacher')[0]
		time = request.args.getlist('time')[0]
		loc = request.args.getlist('loc')[0]
		slots = request.args.getlist('slots')[0]
		courseno = request.args.getlist('id')[0]
		db.execute("update classes set name=?, teacher=?, timeblock=?, location=?, slots=? where courseno=?", (classname, teacher, time, loc, slots, courseno,))
		conn.commit()
		conn.close()
	return render_template('classes.html', classes=libschedule.classes_list())	
@app.route('/classes/delete', methods=['GET', 'POST'])
def classes_delete_page():
	if request.args.getlist('delid'):
		delid = request.args.getlist('delid')[0]
		conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
		db = conn.cursor()
		db.execute("delete from classes where courseno = ?", (delid,))
		conn.commit()
		conn.close()
	return render_template('classes.html', classes=libschedule.classes_list())

@app.route('/classes/add', methods=['GET', 'POST'])
def classes_add_page():
	gets = request.args.getlist
	if gets('name') and gets('teacher') and gets('class') and gets('location') and gets('slots') and gets('id'):
		conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
		db = conn.cursor()
		classname = request.args.getlist('name')[0]
		teacher = request.args.getlist('teacher')[0]
		time = request.args.getlist('class')[0]
		loc = request.args.getlist('location')[0]
		slots = request.args.getlist('slots')[0]
		courseno = request.args.getlist('id')[0]
		db.execute("insert into classes VALUES(?, ?, ?, ?, ?, ?)", (courseno, classname, teacher, time, loc, slots,))
		conn.commit()
		conn.close()
	return render_template('classes.html', classes=libschedule.classes_list())

@app.route('/debug', methods=['GET', 'POST'])
def le_debug():
	raise
	return 'Ohnoes'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

