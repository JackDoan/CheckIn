import npyscreen, curses, sqlite3

class MainForm(npyscreen.FormWithMenus):
  def create(self):
    self.keypress_timeout = 10
    self.i = 0
    self.add(npyscreen.MultiLineEdit, value = """ ____                       _   _   _                 _                      \n|  _ \  ___   __ _ _ __    / \ | |_| |_ ___ _ __   __| | __ _ _ __   ___ ___ \n| | | |/ _ \ / _` | '_ \  / _ \| __| __/ _ \ '_ \ / _` |/ _` | '_ \ / __/ _ \\\n| |_| | (_) | (_| | | | |/ ___ \ |_| ||  __/ | | | (_| | (_| | | | | (_|  __/\n|____/ \___/ \__,_|_| |_/_/   \_\__|\__\___|_| |_|\__,_|\__,_|_| |_|\___\___|""", max_height=5, editable=False)
    self.tagCount()
    self.add(npyscreen.FixedText, editable=False, value=self.statusline, rely=8)
    self.log = self.add(npyscreen.Pager, editable=True, name="Activity Log", values=["Test", "Entry", "123"], rely=10, max_width=95)
    self.add(npyscreen.MultiLineEdit, editable=True, name="External Display", value="", rely=2, relx=100, max_height=6)
    self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application
    self.log.value="potato"
    # The menus are created here.
    self.mtag = self.add_menu(name="Tag Management", shortcut="t")
    self.mtag.addItemsFromList([
      ("lol test", self.logspam),
      ("Look Up Tag", self.tagLookup),
      ("Register New Tag", self.tagReg),
      ("Alter Tag Association", self.tagAlter),
      ("Delete Tag", self.tagDelete)
    ])
    self.mquit = self.add_menu(name="Quit", shortcut="q")
    self.mquit.addItemsFromList([
      ("Log Out", self.logOut),
      ("Exit Application", self.exit_application),
    ])

     # self.m3 = self.mquit.addNewSubmenu("A sub menu", "^F")
     # self.m3.addItemsFromList([
     #   ("Just Beep",   self.whenJustBeep),
     # ])
  def while_waiting(self):
     self.logspam()    
  def logspam(self):
     self.i = self.i +1
     self.log.values.append(self.i)
     self.display()
  def tagLookup(self):
    self.parentApp.setNextForm("LOOKUP")
    self.editing = False
    self.parentApp.switchFormNow()
  def tagReg(self):
    pass
  def tagAlter(self):
    pass
  def tagDelete(self):
    pass
  def tagCount(self):
    self.conn = sqlite3.connect('datt.db')
    self.db = self.conn.cursor()
    self.db.execute("SELECT Count(*) FROM students")
    self.statusline = "[ DoanAttendance Alpha | v0.1 | " + str(self.db.fetchone()[0]) + " students ]"
  def logOut(self):
    self.parentApp.setNextForm("LOGIN")
    self.editing = False
    self.parentApp.switchFormNow()


  def exit_application(self):
    self.parentApp.setNextForm(None)
    self.editing = False
    self.parentApp.switchFormNow()
