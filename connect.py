#!/usr/bin/env python3
#   -*- coding: utf8 -*-
#
#   HideMyPython! - A parser for the free proxy list on HideMyAss!
#
#   This file is used to connect to the HideMyAss! proxy list
#   The first function creates the suitable POST request from the arguments
#   given on the command line.
#   The second function is used to GET/POST data.
#
#   Copyright (C) 2013 Yannick Méheut <useless (at) utouch (dot) fr>
# 
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

def build_post_request(args):
    post_request = {}

    # We build the countries parameter
    for i, country in enumerate(args.countries_list):
        post_request['c[{0}]'.format(i)] = country

    # We build the ports parameter
    post_request['p'] = args.ports

    # We build the protocols parameter
    protocol_codes = {'http' : 0, 'https' : 1, 'socks' : 2}
    for i, protocol in enumerate(args.protocols):
        post_request['pr[{0}]'.format(i)] = protocol_codes[protocol]

    # We check if the "keep alive" flag was raised by the user
    max_anonymity_level = 5 if args.keep_alive else 4
    # We build the anonymity level
    for anonymity in range(args.anonymity, max_anonymity_level):
        index = anonymity - args.anonymity
        post_request['a[{0}]'.format(index)] = anonymity
    
    # We build the speed level
    for speed in range(args.speed, 4):
        index = speed - args.speed
        post_request['sp[{0}]'.format(index)] = speed

    # We build the connection time level
    for connection_time in range(args.connection_time, 4):
        index = connection_time - args.connection_time
        post_request['ct[{0}]'.format(index)] = connection_time

    # TODO add parameter to order/number of result
    post_request['s'] = 0
    post_request['o'] = 0
    post_request['pp'] = 2
    post_request['sortBy'] = 'date'

    # We return the request
    return post_request

def send_data(url, data=None, cookies=None, allow_redirects=True):
    # If we have data, we POST
    if data:
        r = requests.post(url, data=data, cookies=cookies,
                allow_redirects=allow_redirects)
    # Otherwise, we GET
    else:
        r = requests.get(url, cookies=cookies, allow_redirects=allow_redirects)

    return r

