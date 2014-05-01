#!/usr/bin/env python
import sqlite3, time, libcheckinweb
from functools import wraps
chn = libcheckinweb

def attendance_records():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from records order by rowid desc")
	records = map(list, db.fetchall())
	classblocks = chn.get_config()
	for r in records[:]:
		db.execute("Select name from students where rowid=?", (r[1],))
		r[1] = str(db.fetchone()[0])
		if r[4] == "Test":
			classtime = int(time.strftime('%H%M', time.localtime(r[3]))) 
			if classtime >= int(classblocks[0][1] - 48) and classtime <= classblocks[0][1]: #TODO: -8 accounts for 1st grace period
				status = "Present for " + classblocks[0][0]
			elif classtime >= classblocks[0][2] and classtime <= classblocks[1][1]:
				status = "Present for " + classblocks[1][0]
	#		elif classtime >= classblocks[1][2] and classtime <= classblocks[2][1]:
	#			status = "Present for " + classblocks[2][0]
	#		elif classtime >= classblocks[2][2] and classtime <= classblocks[3][1]:
	#			status = "Present for " + classblocks[3][0]
	#		elif classtime >= classblocks[3][2] and classtime <= classblocks[4][1]:
	#			status = "Present for " + classblocks[4][0]
			elif classtime > classblocks[0][1] and classtime < classblocks[0][2]:
			#	tardyby = str(classtime - classblocks[0][1])
			#	tardyby = '{:0>4}'.format(tardyby)				####TODO? add tardyby times
			#	tardyby = tardyby[0] + tardyby[1] + ':' + tardyby[2] + tardyby[3]
				status = 'Tardy for ' + classblocks[0][0]
			elif classtime > classblocks[1][1] and classtime < classblocks[1][2]:
				status = 'Tardy for ' + classblocks[1][0]
	#		elif classtime > classblocks[2][1] and classtime < classblocks[2][2]:
	#			status = 'Tardy for ' + classblocks[2][0]
	#		elif classtime > classblocks[3][1] and classtime < classblocks[3][2]:
	#			status = 'Tardy for ' + classblocks[3][0]
	#		elif classtime > classblocks[4][1] and classtime < classblocks[4][2]:
	#			status = 'Tardy for ' + classblocks[4][0]
			else:
				status = 'OOB: record at ' + str(classtime)

			db.execute('update records set status=? where rowid=?', (status, r[0]))
			r[4] = chn.status_color(status)
		else:
			#	records.remove(r)	removes OOB errors from display -- commented out for testing.
			r[4] = chn.status_color(r[4])

		r[3] = chn.epochToString(r[3])
	conn.commit()
	conn.close()
	return records

def newstudentPage(student_id):
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
	conn.close()
	return [s.classes, classblocks, classlist, records, student_id, s.tag, s.name]

def student_list():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select rowid,* from students")
	students = map(list, db.fetchall())
	conn.close()
	newid = students[-1][0]+1
	return [students, newid]

def student_add(newstudent, newtag):
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
		return [students, newid]
	else:
		conn.close()
		return [students, newid]


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
	return [newid, students]

def student_edit(sid, tag):
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Update `students` set `tag`=? WHERE `rowid`=?;", (tag, sid,))
	db.execute("Select rowid,* from students")
	students = db.fetchall()
	conn.commit()
	conn.close()
	newid = students[-1][0]+1
	return [newid, students]
