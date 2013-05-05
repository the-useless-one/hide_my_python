# HideMyPython!
	 _    _ _     _      __  __       _____       _   _                 _ 
	| |  | (_)   | |    |  \/  |     |  __ \     | | | |               | |
	| |__| |_  __| | ___| \  / |_   _| |__) |   _| |_| |__   ___  _ __ | |
	|  __  | |/ _` |/ _ \ |\/| | | | |  ___/ | | | __| '_ \ / _ \| '_ \| |
	| |  | | | (_| |  __/ |  | | |_| | |   | |_| | |_| | | | (_) | | | |_|
	|_|  |_|_|\__,_|\___|_|  |_|\__, |_|    \__, |\__|_| |_|\___/|_| |_(_)
								 __/ |       __/ |                        
								|___/       |___/                         

A parser for the free proxy list on HideMyAss!

Fork me on [GitHub](https://github.com/the-useless-one/hide_my_python)

## HISTORY

## REQUIREMENTS

All you need is Python, and the PycURL library.

## USAGE

Just go to the `hide_my_python` directory and type
the following command:

    ./hide_my_python.py -o <output_file>

where `output_file` is the database file where the proxies will be stored.

Don't forget to make the script executable with:

    chmod +x hide_my_python.py

To see a list of the options, just issue:

	./hide_my_python -h
	usage: hide_my_python [-h] -o DATABASE_FILE [-ct COUNTRIES_FILE]
	                      [-p PORTS [PORTS ...]]
						  [-pr {http,https,socks} [{http,https,socks} ...]] [-a]
						  [-s] [-c]

	A parser to retrieve proxies from HideMyAss!

	optional arguments:
	  -h, --help            show this help message and exit
	  -o DATABASE_FILE      database file where the proxies will be saved
	  -ct COUNTRIES_FILE    file containing the countries where the proxies can be
							based (default: countries_all)
	  -p PORTS [PORTS ...]  list of ports (max: 20 ports) the proxies listen on
	                    	(default: every port)
	  -pr {http,https,socks} [{http,https,socks} ...]
	                        protocols used by the proxies (default: HTTP, HTTPS
							and SOCKS4/5)
	  -a                    flag used to determine the proxies minimum anonymity
							level, e.g. -a sets the minimum anonymity level to
							Low, -aa to Medium, -aaa to High, etc. (default
							minimum level: None)
	  -s                    flag used to determine the proxies minimum speed
							level, e.g. -s sets the minimum speed level to Medium,
							-ss to Fast (default minimum level: Slow)
	  -c                    flag used to determine the proxies minimum connection
	                        time level, e.g. -c sets the minimum connection time
							level to Medium, -cc to Fast (default minimum level:
							Slow)

	Go to https://hidemyass.com/proxy-list/ to see the different available
	options.

### `database_file`

### `countries_file`

### `ports`

### `protocols`

### `anonymity`

### `speed`

### `connection_time`

## COPYRIGHT

HideMyPython! - A parser for the free proxy list on HideMyAss!

Yannick Méheut

Copyright © 2013

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
Public License for more details.

You should have received a copy of the GNU General Public License along 
with this program. If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
