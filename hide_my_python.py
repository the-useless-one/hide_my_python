#!/usr/bin/env python3
# 	-*- coding: utf8 -*-
#
# 	HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#	This file contains the main function of the HideMyPython! script.
#	It parses the arguments, creates a database, and save the proxies.
#
# 	Copyright (C) 2013 Yannick Méheut <useless@utouch.fr>
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
import arguments
import parser
import database

def main():
	# We create an argument parser
	arg_parser = arguments.create_argument_parser()

	# We parse the arguments
	args = arg_parser.parse_args(sys.argv[1:])
	arguments.process_arguments(args, arg_parser)

	# If the verbose mode is on, we display the arguments
	if args.verbose:
		arguments.print_arguments(args)

	# We open the database file where the proxies will be stored
	connection, cursor = database.initialize_database(args.database_file)

	try:
		# We generate the proxies
		for proxy in parser.generate_proxy(args):
			# And we store them in the database
			database.insert_in_database(cursor, proxy)
	except KeyboardInterrupt:
		if args.verbose:
			print('')
			print('[warn] received interruption signal')

	# We save the changes made to the database, and close the file
	connection.commit()
	connection.close()

	return 0

if __name__ == '__main__':
	main()

