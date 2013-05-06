#!/usr/bin/env python
# -*- coding: utf8 -*-

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
COUNTRY_HTML = re.compile(r'<span class="country">.*?</span>')

# This regex is used to recover the country
COUNTRY = re.compile(r'/> ([a-zA-Z, ]*)')

# This regex is used to recover the HTML code containing the speed in the
# proxy HTML code
SPEED_HTML = re.compile(r'<div class="speedbar response.*?>(.*?)</div>',
		flags=re.DOTALL)
# This regex is used to recover the speed
SPEED = re.compile(r'class="(.*?)"')

# This regex is used to recover the HTML code containing the connection time in
# the proxy HTML code
CONNECT_TIME_HTML = re.compile(r'<div class="speedbar response.*?>(.*?)</div>',
		flags=re.DOTALL)
# This regex is used to recover the connection time
CONNECT_TIME = re.compile(r'class="(.*?)"')

# This regex is used to recover the type and anonymity level in the proxy
# HTML code
TYPE_ANONYMITY = re.compile(r'<td>(.*?)</td>\s*<td.*?>(.*)</td>')

