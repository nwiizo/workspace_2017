#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup


url = "http://192.168.16.128/WackoPicko/"


page = urllib.request.urlopen(url)
s_p = page.read()
s = BeautifulSoup(s_p,"html.parser")
a_list = s.findAll("a")

for a in a_list:
	print (a.get("href"))
