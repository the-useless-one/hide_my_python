#!/usr/bin/env python3
# 	-*- coding: utf8 -*-
#
# 	HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#	This file defines the different needed regular expressions to retrieve
#	the proxy's parameters from the HideMyAss! proxy list.
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

# This regex corresponds to the HTML code describing a proxy
PROXY_HTML = re.compile(r'<tr class=".*?</tr>', flags=re.DOTALL)

# This regex corresponds to the HTML code containing the IP:port of a proxy
IP_PORT_HTML = re.compile(r'<td><span><style>.*?</td>\s*<td>.*?</td>',
		flags=re.DOTALL)

# This regex is used to find the class which won't be displayed in the IP:port
# HTML code
DISPLAY_NONE_CLASS = re.compile(r'([a-zA-Z0-9_-]+){display:none}')

# This regex is used to delete everything between <script> and </script> in
# the IP:port HTML code
STYLE = re.compile(r'<style>.*</style>', flags=re.DOTALL)

# This regex is used to delete everything with a style "display:none" in the
# IP:port HTML code
DISPLAY_NONE = re.compile(r'<[^>]*style="display:none">[^<]*<[^>]*>')

# This regex is used to delete everything between a < and a > in the IP:port
# HTML code
TAGS = re.compile(r'<[^>]*>')

# This regex is used to recover the HTML code containing the country in the
# proxy HTML code
COUNTRY_HTML = re.compile(r'<span class="country".*?>.*?</span>',
        re.DOTALL)

# This regex is used to recover the country
COUNTRY = re.compile(r'([a-zA-Z, ]*)</span>')

# This regex is used to recover the HTML code containing the speed in the
# proxy HTML code
SPEED_HTML = re.compile(r'<div class="progress-indicator.*?levels="speed" rel.*?>(.*?)</div>',
		flags=re.DOTALL)
# This regex is used to recover the speed
SPEED = re.compile(r'style="width: (\d+)%')

# This regex is used to recover the HTML code containing the connection time in
# the proxy HTML code
CONNECT_TIME_HTML = re.compile(r'<div class="progress-indicator.*?levels="speed">(.*?)</div>',
		flags=re.DOTALL)
# This regex is used to recover the connection time
CONNECT_TIME = re.compile(r'style="width: (\d+)%')

# This regex is used to recover the type and anonymity level in the proxy
# HTML code
TYPE_ANONYMITY = re.compile(r'<td>(.*?)</td>\s*<td.*?>(.*)</td>')

