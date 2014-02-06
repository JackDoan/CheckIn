import serial, os, time, datetime, datt, sqlite3

line = []

conn = sqlite3.connect("datt.db")
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

datt.beep()
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
       print("Looking up ID " + linestr)
       db.execute("select * from students where tag = ?", (linestr,))
       print(str(db.fetchone()))
       line = []
       break

 else:
   line = raw_input("Student ID: ")
   print("Looking up ID " + line)
   db.execute("select * from students where tag = ?", (line,))
   student = str(db.fetchone()[0])[0:19]
   print(student)
   datt.lcdClearRow(2)
   datt.lcdRow(2)
   datt.lcdWrite(student)
ser.close()
