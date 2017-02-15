#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup



payload = {'username': 'scanner1', 'password': 'scanner1'}
r = requests.post("http://192.168.56.101/WackoPicko/users/login.php", data=payload)

s=BeautifulSoup(r.text)
a_list=s.findAll("span")

for n in a_list:
        print n
