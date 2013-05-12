#!/usr/bin/env python3
# 	-*- coding: utf8 -*-
#
# 	HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#	This file is used to parse the result page from the HideMyAss! proxy list.
#	The parse_ functions retrieve the proxy's parameters.
#	The last function is a generator, which yields proxies.
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

import re
import regex
import connect

def parse_ip_port(ip_port_html):

	# We parse the class which won't be displayed
	display_none_list = regex.DISPLAY_NONE_CLASS.findall(ip_port_html)

	# We delete everything between <style> and </style>
	ip_port_html = regex.STYLE.sub('', ip_port_html)

	# We delete everything wish a style "display:none"
	ip_port_html = regex.DISPLAY_NONE.sub('', ip_port_html)

	# We delete every tag with a class that won't be displayed
	for display_none in display_none_list:
		class_regex = r'<[^>]*class="%s">[^<]*<[^>]*>' % display_none
		ip_port_html = re.sub(class_regex, '', ip_port_html)

	# We delete everything between < and >
	ip_port_html = regex.TAGS.sub('', ip_port_html)

	# We recover the ip and the port
	ip, port = ip_port_html.split()

	return ip, port

def parse_proxy(proxy_html):

	# We get the chunk of code corresponding to the IP:port...
	ip_port_html = regex.IP_PORT_HTML.search(proxy_html).group(0)
	# ...and we parse it
	ip, port = parse_ip_port(ip_port_html)

	# We get the chunk of code corresponding to the country...
	country_html = regex.COUNTRY_HTML.search(proxy_html).group(0)
	# ...and we parse it
	country = regex.COUNTRY.search(country_html).group(1)

	# We get the chunk of code corresponding to the speed...
	speed_html = regex.SPEED_HTML.search(proxy_html).group(1)
	# ...and we parse it
	speed = regex.SPEED.search(speed_html).group(1)

	# We get the chunk of code corresponding to the connection time...
	connection_time_html = regex.CONNECT_TIME_HTML.search(proxy_html).group(1)
	# ...and we parse it
	connection_time = regex.CONNECT_TIME.search(connection_time_html).group(1)

	# We get the chunk of code corresponding to the type and anonymity...
	match = regex.TYPE_ANONYMITY.search(proxy_html)
	# ...and we parse it
	type = match.group(1)
	anonymity = match.group(2)

	# We return a tuple
	return ip, int(port), type, country, anonymity, speed, connection_time

def generate_proxy(args):
	# We build the post request, using the arguments specified by the user
	post_request = connect.build_post_request(args)

	# This variable will be used to retrieve every page
	# of the search result
	page = 0

	# If no maximum number of proxies was given as an argument,
	# we retrieve every proxy
	retrieve_all = (args.number_of_proxies == 0)
	keep_retrieving = True
	number_of_proxies = 0

	# When you do a search, HideMyAss! redirects you to a page.
	# We retrieve the result page's URL
	r = connect.send_data('https://hidemyass.com/proxy-list/',
			data = post_request, allow_redirects=False)
	url = 'https://hidemyass.com{0}'.format(r.headers['Location'])

	# HideMyAss! checks this cookie to see if you're a legit user
	# (and we totally are!)
	cookies = {'PHPSESSID' : r.cookies['PHPSESSID']}

	while keep_retrieving:
		# Even if a page doesn't exist, HideMyAss! doesn't respond
		# with a 404, so we use this boolean to check if any proxy
		# was found on the page
		results_on_page = False

		# We increment the page number
		page += 1

		# We retrieve the result from the page
		r = connect.send_data('{0}/{1}'.format(url, page), cookies=cookies)
		html_content = r.text

		for proxy_html in regex.PROXY_HTML.findall(html_content):
			# A proxy was found on the page
			results_on_page = True

			# We increment the number of proxies
			number_of_proxies += 1

			# If a maximum number of proxies was set and we
			# are above this limit, we stop retrieving proxies
			if (not retrieve_all and
				number_of_proxies > args.number_of_proxies):
				keep_retrieving = False
				break
			# Otherwise, we generate a proxy
			else:
				# If the verbose mode is on, we display how many proxies
				# we've retrieved
				if args.verbose:
					info_msg = 'retrieved {0}'.format(number_of_proxies)
					if args.number_of_proxies > 0:
						info_msg += '/{0} proxies'.format(args.number_of_proxies)
					else:
						info_msg += ' proxies'
					print('\r[info] {0}'.format(info_msg), end='')
				yield parse_proxy(proxy_html)

		# If no results were found on the page,
		# we stop retrieving proxies
		if not results_on_page:
			keep_retrieving = False

