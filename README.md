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

Fork me on [GitHub](https://github.com/the-useless-one/hide_my_python).

## HISTORY

I was reading this article on [the blog of the Blue Shell Group](https://blueshellgroup.wordpress.com/2013/04/14/creating-a-private-database-of-proxies-part-1/),
and I thought at first "Meh, it'll just be parsing". But when I read the second
part of the article, and saw how HideMyAss! didn't want you to parse its proxy
list, the mischief that I am wanted to do nothing else but parse its proxy
list.

So here's my implementation in Python of a parser for the free proxy list on
HideMyAss! I hope someone will find it useful.

## DISCLAIMER

Oh, and I'm not responsible for anything that happens to you or that you do
using these proxies. If someone gets pwned, don't look at me.

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

	./hide_my_python.py -h
	usage: hide_my_python [-h] -o DATABASE_FILE [-ct COUNTRIES_FILE]
	                      [-p PORTS [PORTS ...]]
						  [-pr {http,https,socks} [{http,https,socks} ...]] [-a]
						  [-ka] [-s] [-c]

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
	  -ka                   flag used to determine if proxies with the Keep Alive
							option should be returned, as they are likely honey
							pots (default: no)
	  -s                    flag used to determine the proxies minimum speed
							level, e.g. -s sets the minimum speed level to Medium,
							-ss to Fast (default minimum level: Slow)
	  -c                    flag used to determine the proxies minimum connection
	                        time level, e.g. -c sets the minimum connection time
							level to Medium, -cc to Fast (default minimum level:
							Slow)

	Go to https://hidemyass.com/proxy-list/ to see the different available
	options.

### Database file

The proxies will be saved in this file. If the file doesn't exist, it will be
created. If it exists, the proxies will be appended to it (the file won't be
overwritten). The database contains only one table, named `proxies`, with the
following structure:

* `id`: a unique identifier (type: `INTEGER PRIMARY KEY AUTOINCREMENT`)
* `ip`: the proxy's IP address (type: `TEXT`)
* `port`: the port the proxy listens on (type: `INTEGER`)
* `type`: the type of the proxy (HTTP, HTTPS or SOCKS4/5) (type: `TEXT`)
* `country`: the country the proxy is based in (type: `TEXT`)
* `anonymity`: the anonymity level guarantied by the proxy (type: `TEXT`)
* `speed`: the speed level of the proxy (type: `TEXT`)
* `connection_time`: the connection time of the proxy (type: `TEXT`)

### Countries file

The script will only return proxies based in the countries specified in this
file. To see a complete list of the available countries, see the file
`countries_all`.

### Ports

The script will only return proxies listening on the specified ports. You can
specify up to 20 different ports. For example:

	./hide_my_python.py -p 80 8080 443 -o output.db

will only return proxies listening either on port 80, 8080, or 443.

### Protocols

The script will only return proxies using the specified protocols. The possible
protocols are HTTP, HTTPS, and SOCKS4/5. For example:

	./hide_my_python.py -pr http socks -o output.db

will only return proxies using HTTP or SOCKS4/5.

### Anonymity

The script will only return proxies guarantying an anonymity level greater
than the one specified by the user. HideMyAss! proxies have these anonymity
levels:

* None
* Low
* Medium
* High
* High + Keep Alive

**WARNING:** Here's what HideMyAss! has to say on proxies with Keep Alive:

> If a high-anonymous proxy supports keep-alive you can consider it to be
> extremely-anonymous. However, such a host is highly possible to be a
> honey-pot.

**Use these proxies at your own risk!**

By default, the script doesn't take into account the proxies' anonymity
(they can have an anonymity level of None, High, Medium, ...). But this
command:

	./hide_my_python.py -a -o output.db

will only return proxies with an anonymity level of at least Low.

This command:

	./hide_my_python.py -aa -o output.db

will only return proxies with an anonymity level of at least Medium.

### Keep Alive

As said on the HideMyAss! proxy list, proxies with the Keep Alive option are
most likely honey pots. In order to avoid them, the script, by default, doesn't
retrieve proxies with an anonymity level of High +KA. If you want proxies with
the Keep Alive option, use this flag:

	./hide_my_python.py -ka -o output.db

### Speed

The script will only return proxies guarantying a speed level greater
than the one specified by the user. HideMyAss! proxies have these speed 
levels:

* Slow
* Medium
* Fast

By default, the script doesn't take into account the proxies' speed (they can
have a speed of Slow, Medium, Fast). But this command:

	./hide_my_python.py -s -o output.db

will only return proxies with a speed level of at least Medium.

This command:

	./hide_my_python.py -ss -o output.db

will only return proxies with a speed level of at least Fast.

### Connection time

The script will only return proxies guarantying a connection time level greater
than the one specified by the user. HideMyAss! proxies have these connection
time levels:

* Slow
* Medium
* Fast

By default, the script doesn't take into account the proxies' connection time
(they can have a connection time of Slow, Medium, Fast). But this command:

	./hide_my_python.py -c -o output.db

will only return proxies with a connection time level of at least Medium.

This command:

	./hide_my_python.py -cc -o output.db

will only return proxies with a connection time level of at least Fast.

## COPYRIGHT

HideMyPython! - A parser for the free proxy list on HideMyAss!

Yannick Méheut [<useless@utouch.fr>] - Copyright © 2013

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
