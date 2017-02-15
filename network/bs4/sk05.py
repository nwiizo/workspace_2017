#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
import sys
import urllib2

def login_a():
	url = "http://192.168.56.101/WackoPicko/users/login.php"
	page = urllib2.urlopen(url)
	s_p = page.read()
	s = BeautifulSoup(s_p)
	a_list = s.findAll("input")

	for n in a_list:
        	name = n.get("usename")
	

def login_b():
	payload = {'username': str(sys.argv[1]), 'password': str(sys.argv[2])}
	r = requests.post("http://192.168.56.101/WackoPicko/users/login.php", data=payload)

	s=BeautifulSoup(r.text)
	a_list=s.findAll("span")

	for n in a_list:
       		print n



print login_a()
