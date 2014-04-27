import sqlite3, time

def epochToString(epoch):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

class Student:
	def __init__(self, student_id):
		conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
		db = conn.cursor()
		db.execute("Select rowid,* from students where `rowid`=?", (student_id,))
		result = db.fetchall()
		conn.close()
		if result:
			result = result[0]
			self.student_id = result[0]
			self.name = result[1]
			self.tag = result[2]
			self.classes_string = str(result[3])
			self.classes = self.classes_string.split(',')
