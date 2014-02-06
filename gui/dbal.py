import sqlite3

class dbal():
  conn = sqlite3.connect("datt.db")
  db = conn.cursor

  def addTag(self, name, tval):
    self.db.execute('INSERT INTO students VALUES (?,?)', (name, tval))
    self.conn.commit()

  def lookupSingle(self, table, col, val):
    self.db.execute('SELECT * FROM ? WHERE ?=?', (table, col, val))
    self.results = self.db.fetchall()
    if len(self.results) > 1:
      self.baddata = 1
    return self.results.pop()

  def update(self, table, toEdit, newVal, dCol, dVal):
    self.db.execute('UPDATE ? SET ? = ? WHERE ? = ?', (table, toEdit, newVal, dCol, dVal))
    self.conn.commit
