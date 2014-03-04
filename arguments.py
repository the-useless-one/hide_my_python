#!/usr/bin/env python3
# 	-*- coding: utf8 -*-
#
# 	HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#	This file is used to parse the arguments.
#	The first function creates a parser that will retrieve the arguments from
#	the command line.
#	The second function processes the arguments (checks the given values etc.)
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

import os
import sys
import argparse

def create_argument_parser():
	arg_parser = argparse.ArgumentParser(
			prog='hide_my_python',
			description='A parser to retrieve proxies from HideMyAss!',
			epilog='Go to https://hidemyass.com/proxy-list/ to see the '
					'different available options.')

	# The user has to specify an output file
	arg_parser.add_argument('-o', dest='database_file', type=str,
			required=True,
			help='database file where the proxies will be saved')

	# The user can specify a maximum number of proxies to retrieve
	arg_parser.add_argument('-n', dest='number_of_proxies', type=int,
			default=0,
			help='maximum number of proxies to retrieve (default: all)')

	# The user can specify a list of countries
	arg_parser.add_argument('-ct',
            default='{0}/countries_all'.format(os.path.dirname(sys.argv[0])),
			dest='countries_file', type=argparse.FileType('r'),
			help='file containing the countries where the '
					'proxies can be based (default: %(default)s)')

	# The user can specify a list of ports
	arg_parser.add_argument('-p', type=int, nargs='+', dest='ports',
			help='list of ports (max: 20 ports) the proxies listen on '
					'(default: every port)')

	# The user can specify a list of protocols
	arg_parser.add_argument('-pr', type=str, nargs='+',
			choices=['http', 'https', 'socks'], dest='protocols',
			help='protocols used by the proxies '
					'(default: HTTP, HTTPS and SOCKS4/5)')

	# The user can specify the anonymity level
	arg_parser.add_argument('-a', default=0, action='count', dest='anonymity',
			help='flag used to determine the proxies minimum anonymity '
					'level, e.g. -a sets the minimum anonymity level to Low, '
					'-aa to Medium, -aaa to High, etc. (default minimum level: '
					'None)')

	arg_parser.add_argument('-ka', action='store_true',
			dest='keep_alive',
			help='flag used to determine if proxies with the Keep Alive '
					'option should be returned, as they are likely honey pots '
					'(default: no)')

	# The user can specify the required speed
	arg_parser.add_argument('-s', default=1, action='count', dest='speed',
			help='flag used to determine the proxies minimum speed '
					'level, e.g. -s sets the minimum speed level to Medium, '
					'-ss to Fast (default minimum level: Slow)')

	# The user can specify the connection time
	arg_parser.add_argument('-c', default=1, action='count',
			dest='connection_time',
			help='flag used to determine the proxies minimum connection time '
					'level, e.g. -c sets the minimum connection time level to '
					'Medium, -cc to Fast (default minimum level: Slow)')

	arg_parser.add_argument('-v', action='store_true', dest='verbose',
			help='explain what is being done')

	return arg_parser

def process_arguments(args, arg_parser):

	# If the given number of proxies is negative,
	# we return an error
	if args.number_of_proxies < 0:
		error_msg = 'argument {0}: invalid value '\
				+ '(a positive integer is required): {1}'
		error_msg = error_msg.format('-n', args.number_of_proxies)
		arg_parser.error(error_msg)

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
			error_msg = 'argument {0}: invalid value '\
					+ '(maximum 20 ports): {1} ports given'
			error_msg = error_msg .format('-p', len(args.ports))
			arg_parser.error(error_msg)
		# Otherwise, we create a comma-separated string
		else:
			ports_string = ''
			for port in args.ports:
				# If the port is in the good range, we add it
				if 1 <= port and port <= 65535:
					ports_string += '{0}, '.format(port)
				# Otherwise, we raise an error
				else:
					error_msg = 'argument {0}: invalid value '\
							+ '(port must be between 1 and 65535): {1}' 
					error_msg = error_msg .format('-p', port)
					arg_parser.error(error_msg)
				# We delete the last comma
			ports_string = ports_string[:-2]
			args.ports = ports_string
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

def print_arguments(args):
	# We display the number of proxies
	if args.number_of_proxies > 0:
		number = args.number_of_proxies
	else:
		number = 'all'
	print('[info] number of proxies: {0}'.format(number))

	# We display the first five countries
	if len(args.countries_list) <= 5:
		countries = args.countries_list
	else:
		countries = '{0} and {1} more' 
		countries = countries.format(args.countries_list[0:5],
				len(args.countries_list) - 5)
	print('[info] countries: {0}'.format(countries))

	# We display the ports
	if args.ports:
		ports = args.ports
	else:
		ports = 'all'
	print('[info] ports: {0}'.format(ports))

	# We display the protocols
	print('[info] protocols: {0}'.format(args.protocols))

	# We display the anonymity levels
	anonymity_levels = ['None', 'Low', 'Medium', 'High']
	if args.keep_alive:
		anonymity_levels.append('High +KA')
	print('[info] anonymity: {0}'.format(
		anonymity_levels[args.anonymity:]))

	# We display the speed levels
	speed_levels = ['Slow', 'Medium', 'High']
	print('[info] speed: {0}'.format(speed_levels[args.speed:]))

	# We display the speed levels
	connection_time_levels = ['Slow', 'Medium', 'High']
	print('[info] connection time: {0}'.format(
		connection_time_levels[args.connection_time:]))

