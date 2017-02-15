#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import BeautifulSoup


url = "http://192.168.56.101/WackoPicko/"
page = urllib2.urlopen(url)
s_p = page.read()
s = BeautifulSoup(s_p)
print(s.findAll("title")[0])

