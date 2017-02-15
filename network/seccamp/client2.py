#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup


url = "http://127.0.0.1:8000/cgi-bin/index.py"


page = urllib.urlopen(url)
s_p = page.read()
s = BeautifulSoup(s_p)
a=[]
for form in s.findAll("input"):
	a = form
	print a
