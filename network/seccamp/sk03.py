#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import BeautifulSoup


url = "http://192.168.56.101/peruggia/"
tag=["a","link","script","import"]

def test(url,tag):
	page = urllib2.urlopen(url)
	s_p = page.read()
	s = BeautifulSoup(s_p)
	a_list=s.findAll(tag)

	for n in a_list:
			print url+n.get("href")

for n in tag:
	test(url,n)

