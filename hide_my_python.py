#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import arguments
import parser
import database

def main():
	# We create an argument parser
	arg_parser = arguments.create_argument_parser()

	# We parse the arguments
	args = arg_parser.parse_args(sys.argv[1:])
	arguments.process_arguments(args, arg_parser)

	# We open the database file where the proxies will be stored
	connection, cursor = database.initialize_database(args.database_file)

	# We generate the proxies
	for proxy in parser.generate_proxy(args):
		print(proxy)
		# And we store them in the database
		database.insert_in_database(cursor, proxy)

	# We save the changes made to the database, and close the file
	connection.commit()
	connection.close()

	return 0

if __name__ == '__main__':
	main()

