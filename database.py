#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import sqlite3

def insert_in_database(cursor, proxy):

	# We check if the prxoy is already in the database
	cursor.execute('SELECT id FROM proxies WHERE ip=? and port=?', proxy[0:2])

	# If it is, we don't store it
	if cursor.fetchone():
		return

	# Otherwise, we save it
	cursor.execute('INSERT INTO proxies (ip, port, type, country, anonymity,\
			speed, connection_time) VALUES (?, ?, ?, ?, ?, ?, ?)', proxy)	

def initialize_database(database_file):
	# We connect to the database file
	connection = sqlite3.connect(database_file)
	cursor = connection.cursor()

	# We create the table where the proxies will be stored
	try:
		cursor.execute('CREATE TABLE proxies (id INTEGER PRIMARY KEY\
				AUTOINCREMENT, ip TEXT, port INTEGER, type TEXT, country TEXT,\
				anonymity TEXT, speed TEXT, connection_time TEXT)')
	# If there's already such a table, we don't have anything to do
	except sqlite3.OperationalError:
		pass
	# Otherwise, we save the changes
	else:
		connection.commit()
	
	# We return the connection to the database
	return connection, cursor

