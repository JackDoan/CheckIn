#!/usr/bin/env python
import serial, os, time, datetime, datt, sqlite3

line = []


loc = "D117"
status = "Test"
conn = sqlite3.connect("./datt.db")
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
         timeout=0)
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
	os.system("gpio export 40")
	os.system("gpio export 41")
	os.system("gpio export 4")
	os.system("gpio dir 40 out")
	os.system("gpio dir 41 out")
	os.system("gpio dir 4 out")
	os.system("gpio write 40 0")
	os.system("gpio write 41 0")
	os.system("gpio write 4 1")
	datt.beep()
	ip = os.popen("ifconfig wlan0 | grep inet | awk '{print $2}' | sed -e s/.:/*/").read()
	datt.lcdClear()
	datt.lcdRow(0)
	datt.lcdWrite("IP Address:")
	datt.lcdRow(1)                                                                   
	datt.lcdWrite(ip[4:-1])
	os.system("sleep 3")
	datt.lcdClear()
	datt.lcdWrite("Checkin v0.1")
	datt.lcdRow(1)
	datt.lcdWrite("Doan Engineering")

while True:
	if noSerial == 0:
		for c in ser.read():
			line.append(c)
			if c == '\n':
				datt.beep()
				datt.lcdClear()
			if '\x03' in line:
				line.remove('\x03')
			if '\x02' in line:
				line.remove('\x02')
			if '\r' in line:
				line.remove('\r')
			if '\n' in line:
				line.remove('\n')
			linestr = ''.join(line)
			line = []
			break
	else:
		linestr = raw_input("Student ID: ")

	print("Looking up ID " + linestr)
	db.execute("select rowid,* from students where tag = ?", (linestr,))
	result = db.fetchone()
	if result:
		student = str(result[1])[0:15]
		student_id = result[0]
                print("Found student ID " + str(student_id) + " named " + student)
		scantime = time.time()
		db.execute("INSERT INTO `records` (`student_id`, `location`, `time`, `status`) VALUES (?, ?, ?, ?);", (student_id, loc, scantime, status,))
		conn.commit()
                print("Record stored at: " + str(scantime))
	else:
		print "No result"
		student = "Tag not assigned!"
		fail = 1

	if noSerial == 0:
		datt.lcdClear()
		datt.lcdRow(0)
		if fail == 1:
			datt.lcdWrite("ERROR")
		else:  
			datt.lcdWrite("Welcome to class")                                             
		datt.lcdRow(1)
		datt.lcdWrite(student)

ser.close()
