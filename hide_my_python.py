#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import argparse
import connect
import parser
import database

def main():
	arg_parser = argparse.ArgumentParser(
			prog='hide_my_python',
			description='A parser to retrieve proxies from HideMyAss!',
			epilog='Go to https://hidemyass.com/proxy-list/ to see the\
					different available options.')

	# The user has to specify an output file
	arg_parser.add_argument('-o', dest='database_file', type=str,
			required=True,
			help='database file where the proxies will be saved')

	# The user can specify a list of countries
	arg_parser.add_argument('-ct', default='countries_all',
			dest='countries_file', type=argparse.FileType('r'),
			help='file containing the countries where the\
					proxies can be based (default: %(default)s)')

	# The user can specify a list of ports
	arg_parser.add_argument('-p', type=int, nargs='+', dest='ports',
			help='list of ports (max: 20 ports) the proxies listen on\
					(default: every port)')

	# The user can specify a list of protocols
	arg_parser.add_argument('-pr', type=str, nargs='+',
			choices=['http', 'https', 'socks'], dest='protocols',
			help='protocols used by the proxies\
					(default: HTTP, HTTPS and SOCKS4/5)')

	# The user can specify the anonymity level
	arg_parser.add_argument('-a', default=0, action='count', dest='anonymity',
			help='flag used to determine the proxies minimum anonymity\
					level, e.g. -a sets the minimum anonymity level to Low,\
					-aa to Medium, -aaa to High, etc. (default minimum level:\
					None)')

	# The user can specify the required speed
	arg_parser.add_argument('-s', default=1, action='count', dest='speed',
			help='flag used to determine the proxies minimum speed\
					level, e.g. -s sets the minimum speed level to Medium,\
					-ss to Fast (default minimum level: Slow)')

	# The user can specify the connection time
	arg_parser.add_argument('-c', default=1, action='count',
			dest='connection_time',
			help='flag used to determine the proxies minimum connection time\
					level, e.g. -c sets the minimum connection time level to\
					Medium, -cc to Fast (default minimum level: Slow)')

	# We parse the arguments
	args = arg_parser.parse_args(sys.argv[1:])

	# We retrieve the countries from the given file
	args.countries_list = []
	for country in args.countries_file.readlines():
		country = country.rstrip()
		args.countries_list.append(country)

	# If ports were specified
	if args.ports:
		# We delete the duplicates
		args.ports = list(set(args.ports))
		# If too many ports were specified, we exit with an error
		if len(args.ports) > 20:
			print >>sys.stderr,\
			'error: too many ports specified (max: 20 ports)'
			sys.exit(-1)
		# Otherwise, we create a comma-separated string
		else:
			args.ports = ', '.join(map(str, args.ports))
	# If no ports were specified, we do nothing
	else:
		args.ports = ''

	# If no protocol was specified, we consider every possible protocol
	if not args.protocols:
		args.protocols = ['http', 'https', 'socks']
	# Otherwise, we delete the duplicates
	else:
		args.protocols = list(set(args.protocols))

	# The maximum anonymity level is 4
	if args.anonymity > 4:
		args.anonymity = 4

	# The maximum speed level is 3
	if args.speed > 3:
		args.speed = 3

	# The maximum connection time level is 3
	if args.connection_time > 3:
		args.connection_time = 3

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

