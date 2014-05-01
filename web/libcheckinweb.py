import sqlite3, time

btnblue = '<button type="button" class="btn btn-primary btn-xs">'
btngreen = '<button type="button" class="btn btn-success btn-xs">'
btnyellow = '<button type="button" class="btn btn-warning btn-xs">'


def check_auth(username, password):
	return username == 'admin' and password == 'secret'

def status_color(status):
	if status[0] == 'T':
		status = btnyellow + status
	elif status[0] == 'P':
		status = btngreen + status
	elif status[0] == 'O':
		status = btnblue + status
	return status

#####
# CRUDE HACK TO MAKE PRESENTING SUPER EASY
#####
def get_config():
	return [['School', int(900), int(1610)], ['After-School', int(1900), int(2100)]]

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
