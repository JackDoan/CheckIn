import os, sqlite3

def ttyEcho(cmd):
  """Write a command to /dev/ttyS0"""
  cmd = str(cmd)
  os.system("echo " + cmd + " > /dev/ttyS0")

def beep(): 
  """Send a BEEP signal down the UART to the AVR over the serial port"""
  ttyEcho("BL0")
  ttyEcho("BEEP")
  ttyEcho("BL1")
def lcdClear():
  """Send CLEAR to the AVR to wipe the screen"""
  ttyEcho("CLEAR")

def lcdRow(row):
  """Change to a specific row on the LCD"""
  if row == 0 or 1 or 2 or 3:
    ttyEcho("ROW" + str(row)) 
  else:
    print("You suck, that's not a row.")

def lcdClearRow(row):
  """Clear a specific row on the LCD"""
  if row == 0 or 1 or 2 or 3:
    ttyEcho("ROW" + str(row))
    ttyEcho("\"W                    \"")
  else:
    print("You suck, that's not a row.")

def lcdWrite(words):
  """Write to the LCD"""
  words = str(words)[0:19]
  ttyEcho("W" + words)

def tagLookup(tag):
  """Query the database for the tag ID"""
  
