#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib


url = "http://www.pycon.jp/"

page = urllib.urlopen(url)
s = page.read()
print (s)
