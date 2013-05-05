#!/usr/bin/env python
# -*- coding: utf8 -*-

import pycurl
import StringIO
import urllib
import tempfile

def build_post_request(args):
	post_request = ''

	# We build the countries parameter
	for country in args.countries_list:
		post_request += '&' + urllib.quote_plus('c[]') +\
				('=%s' % urllib.quote_plus(country))

	# We build the ports parameter
	post_request += '&p=%s' % urllib.quote_plus(args.ports)

	# We build the protocols parameter
	for prot in args.protocols:
		if prot == 'http':
			prot_code = 0
		elif prot == 'https':
			prot_code = 1
		else:
			prot_code = 2
		post_request += '&' + urllib.quote_plus('pr[]') + '=%d' % prot_code

	# We build the anonymity level
	for anon in xrange(args.anonymity, 5):
		post_request += '&' + urllib.quote_plus('a[]') + '=%d' % anon
	
	# We build the speed level
	for speed in xrange(args.speed, 4):
		post_request += '&' + urllib.quote_plus('sp[]') + '=%d' % speed

	# We build the connection time level
	for con_time in xrange(args.connection_time, 4):
		post_request += '&' + urllib.quote_plus('ct[]') + '=%d' % con_time

	# TODO add parameter to order/number of result
	post_request += '&s=0&o=0&pp=3&sortBy=date'

	# We delete the first ampersand
	post_request = post_request[1:]

	# We return the request
	return post_request

def send_data(url, data=None):
	# The HTML code will be stored in output
	output = StringIO.StringIO()
	# The curl_object is used to do the request
	curl_object = pycurl.Curl()

	# We configure the curl_object
	curl_object.setopt(pycurl.WRITEFUNCTION, output.write)
	curl_object.setopt(pycurl.URL, url)

	# HideMyAss redirects to the result page, so we have to follow redirections
	curl_object.setopt(pycurl.FOLLOWLOCATION, 1)

	# HideMyAss checks the cookies to see if the user is legitimate
	_, cookie_jar = tempfile.mkstemp(prefix='hmp_cookies_')
	curl_object.setopt(pycurl.COOKIEJAR, cookie_jar)
	curl_object.setopt(pycurl.COOKIEFILE, cookie_jar)

	# If we have something to post, we specify it
	if data != None:
		curl_object.setopt(pycurl.POST, 1)
		curl_object.setopt(pycurl.POSTFIELDS, data)

	# We perform and close
	curl_object.perform()
	curl_object.close()

	# We return the HTML code
	return output.getvalue()

