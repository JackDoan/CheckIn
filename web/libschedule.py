#!/usr/bin/env python
from flask import Flask, render_template, request, Response
import sqlite3, time
from functools import wraps

def get_config():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select * from config;")
	config = db.fetchall()
	conn.close()
	classblocks = []
	for pair in config:
		if pair[0] == "class_blocks":
			blocks = str(pair[1]).split()
			for block in blocks:
				block_start = block + "_start"
				block_end = block + "_end"
				for each in config:
					if each[0] == block_start:
						block_start_time = each[1]
					if each[0] == block_end:
						block_end_time = each[1]
				classblocks.append([block, int(block_start_time), int(block_end_time)])
	return classblocks

def classes_list():
	conn = sqlite3.connect("/usr/local/CheckIn/chn.db")
	db = conn.cursor()
	db.execute("Select * from classes")
	classes = db.fetchall()
	conn.close()
	return classes
