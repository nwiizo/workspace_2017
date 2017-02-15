#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup

def get_link():
	url = "http://127.0.0.1:8000/cgi-bin/index.py"
	page = urllib.request.urlopen(url)
	s_p = page.read()
	s = BeautifulSoup(s_p)
	a=[]
	for form in s.findAll("input"):
		a = form
		print (a)


if __name__ == '__main__':
	get_link()	
