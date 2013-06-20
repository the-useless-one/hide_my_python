#!/usr/bin/env python3
# 	-*- coding: utf8 -*-
#
# 	HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#	This file is used to create the database and the store the proxies in it.
#
# 	Copyright (C) 2013 Yannick Méheut <useless (at) utouch (dot) fr>
# 
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
# 
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
# 
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import sqlite3

def insert_in_database(cursor, proxy):

	# We check if the prxoy is already in the database
	cursor.execute('SELECT id FROM proxies WHERE ip=? and port=?', proxy[0:2])

	# If it is, we don't store it
	if cursor.fetchone():
		return

	# Otherwise, we save it
	cursor.execute('INSERT INTO proxies (ip, port, type, country, anonymity, '
			'speed, connection_time) VALUES (?, ?, ?, ?, ?, ?, ?)', proxy)

def initialize_database(database_file):
	# We connect to the database file
	connection = sqlite3.connect(database_file)
	cursor = connection.cursor()

	# We create the table where the proxies will be stored
	try:
		cursor.execute('CREATE TABLE proxies (id INTEGER PRIMARY KEY '
				'AUTOINCREMENT, ip TEXT, port INTEGER, type TEXT, country TEXT, '
				'anonymity TEXT, speed TEXT, connection_time TEXT)')
	# If there's already such a table, we don't have anything to do
	except sqlite3.OperationalError:
		pass
	# Otherwise, we save the changes
	else:
		connection.commit()
	
	# We return the connection to the database
	return connection, cursor

