#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup


url = "http://192.168.16.128/WackoPicko/users/login.php"


page = urllib.request.urlopen(url)
s_p = page.read()
s = BeautifulSoup(s_p,"html.parser")
for form in s.findAll("input"):
    print(form.get("name"))

