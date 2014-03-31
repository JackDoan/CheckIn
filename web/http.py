#!/usr/bin/env python
from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)
@app.route('/')
def hello_world():
	conn = sqlite3.connect("../datt.db")
        db = conn.cursor()
        db.execute("Select rowid,* from records")
        t_records = db.fetchall()
	records = map(list, t_records)
	i = 0
	for r in records:
	  db.execute("Select name from students where rowid=?", (r[1],))
	  r[1] = str(db.fetchone()[0])
        conn.close()
        return render_template('data.html', records=records)
@app.route('/test')
def test1():
	conn = sqlite3.connect("../datt.db")
	db = conn.cursor()
	db.execute("Select * from students")
	studentnames = db.fetchall()
	conn.close()
	return render_template('test.html', studentnames=studentnames)

if __name__ == '__main__':
	app.debug = True
	app.run()

