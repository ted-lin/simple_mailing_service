#!/usr/bin/env python

import sqlite3

#db variable
techcrunch_db = 'techcrunch.db'
conn = []
c = []
success = True
err_duplicate = False

def db_init(db=techcrunch_db):
	global conn
	global c
	conn = sqlite3.connect(db)
	c = conn.cursor()

def db_create_table_if_not_exists(table):
	sql = 'create table if not exists ' + table + '(url text, unique(url))'
	c.execute(sql)
	conn.commit()

def db_insert_url(url, table):
	ret = success
	u = (url,)
	sql = 'insert into ' + table + ' values (?)'
	try:
		c.execute(sql, u)
	except sqlite3.IntegrityError:
		ret = err_duplicate
	except sqlite3.Error as e:
		print e
	conn.commit()
	return ret

def db_commit():
	conn.commit()

def db_close():
	conn.close()

if __name__ == "__main__":
	# test code
	db_init('gg')
	db_create_table_if_not_exists('urls')
	db_insert_url('http://www.google.com', 'urls')
	db_insert_url('http://tw.yahoo.com', 'urls')
	db_insert_url('http://www.google.com', 'urls')
	db_insert_url('http://www.google.com', 'urls')
	db_close()
