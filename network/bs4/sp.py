# -*- coding: utf-8 -*-
#%!/bin/bash python3

import lxml.html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

# 新規タブをあけるキー操作を設定
newtab=Keys.CONTROL + 't'

driver = webdriver.Firefox()

slist=["Python","sprint"]

for xkey in slist:
	driver.get("https://www.google.co.jp/")
	driver.find_element_by_name("p").clear()
	driver.find_element_by_name("p").send_keys(xkey)
	driver.find_element_by_css_selector("input.b").click()
#	driver.quit()
body = driver.find_element_by_tag_name("body")
body.send_keys(newtab)

