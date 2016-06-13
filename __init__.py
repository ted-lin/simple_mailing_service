#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
tech crunch parser
"""

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import unicodedata

import db_utils as db

target="http://techcrunch.com"
urls=[]
uniurls=[]

def send_out(url, table):
	if (db.db_insert_url(url, table) == True):
		print 'send out'
	else:
		print 'duplicate'

def unicode2ascii(ustr):
	return unicodedata.normalize('NFKD', ustr).encode('ascii', 'ignore')

def parse_tech_crunch(dump=False):
	global uniurls
	html_page = urllib2.urlopen(target)
	soup = BeautifulSoup(html_page)

	for link in soup.findAll('a', attrs = {'href': re.compile("/[0-9]*/[0-9]*/[0-9]*")}):
		astr=unicode2ascii(link.get('href'))
		if '#' in astr or '?' in astr:
			pass
		else:
			urls.append(astr)

	uniurls = list(set(urls))

	if dump:
		for url in uniurls:
			print url

if __name__ == "__main__":
	table='urls'

	#URL
	parse_tech_crunch()

	#DB
	db.db_init()
	db.db_create_table_if_not_exists(table)

	for url in uniurls:
		print url
		send_out(url, table)

	db.db_close()
