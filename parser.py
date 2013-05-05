#!/usr/bin/env python
# -*- coding: utf8 -*-

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

	# We recover the HTML code
	html = connect.send_data('https://hidemyass.com/proxy-list/', post_request)

	# We find every chunk of code corresponding to a proxy in the HTML code
	proxy_html_iter = regex.PROXY_HTML.finditer(html)
	
	# We parse every proxy HTML code
	for proxy_html in proxy_html_iter:
		yield parse_proxy(proxy_html.group(0))

