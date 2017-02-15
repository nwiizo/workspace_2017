#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import mechanize

url = "http://127.0.0.1:8000/cgi-bin/index.py"

br = mechanize.Browser()
page = br.open(url)

br.select_form(nr=0)
br["name"]="MOTOUCHI"
br["comments"]="hello world"
br.submit()
