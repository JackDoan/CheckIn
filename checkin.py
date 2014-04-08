#!/usr/bin/env python
import serial, os, time, datetime, libcheckin, sqlite3
chn = libcheckin
line = ''
linestr = ''
fail = 0
loc = "D117"
status = "Test"
delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())


conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
db = conn.cursor()
db.execute("Select COUNT(*) from students")
studentCount = str(db.fetchone()[0])
welcomemsg = "Loaded database with " + studentCount + " students"
print(welcomemsg)

noSerial = 0

try:
	ser = serial.Serial(
		port='/dev/ttyS0',\
		baudrate=9600,\
		parity=serial.PARITY_NONE,\
		stopbits=serial.STOPBITS_ONE,\
		bytesize=serial.EIGHTBITS,\
		timeout=None)

except serial.SerialException, e:
	print("could not open serial port!!!")
	noSerial = 1
	class fakeser:
		def read(self):
	  		return [0,0,0,0]
		def close(self):
			pass
	ser = fakeser()

if noSerial == 0:
	chn.beep()
	ip = os.popen("ifconfig wlan0 | grep inet | awk '{print $2}' | sed -e s/....://").read()
	chn.lcdClear()
	chn.lcdRow(0)
	chn.lcdWrite("IP Address:")
	chn.lcdRow(1)
	chn.lcdWrite(str.strip(ip))
	os.system("sleep 3")
	chn.lcdClear()
	chn.lcdWrite("Checkin v0.1")
	chn.lcdRow(1)
	chn.lcdWrite("Doan Engineering")

while True:
	if noSerial == 0:
		line = ser.readline()
		if line:
			linestr = line.translate(None, delchars)
			chn.beep()
			chn.lcdClear()
			line = '' 
	else:
		linestr = raw_input("Student ID: ")

	print("Looking up ID " + linestr)
	db.execute("select rowid,* from students where tag = ?", (linestr,))
	result = db.fetchone()
	linestr = ''

	if result:
		student = str(result[1])[0:15]
		student_id = result[0]
		print("Found student ID " + str(student_id) + " named " + student)
		scantime = time.time()
		db.execute("INSERT INTO `records` (`student_id`, `location`, `time`, `status`) VALUES (?, ?, ?, ?);", (student_id, loc, scantime, status,))
		conn.commit()
		print("Record stored at: " + str(scantime))
		fail = 0
	else:
		print "No result"
		student = "Tag not assigned!"
		fail = 1

	if noSerial == 0:
		chn.lcdClear()
		chn.lcdRow(0)
		if fail == 1:
			chn.lcdWrite("ERROR")
		else:  
			chn.lcdWrite("Welcome to class")											 
		chn.lcdRow(1)
		chn.lcdWrite(student)

ser.close()
