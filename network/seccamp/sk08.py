#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from BeautifulSoup import BeautifulSoup
import mechanize


token = ""
user_agent = {'User-agent': 'Mozilla/5.0'}
r = requests.get("http://192.168.56.102/signin",headers=user_agent)
cookie_token = r.cookies["csrf_token"]
soup = BeautifulSoup(r.text)
input_list = soup.findAll('input')

for input in input_list:
	if input.get("name") == "csrf_token":
		token = input.get("value")

payload = {'username': 'test', 'password': 'testtest', 'csrf_token': token}
cookies = dict(csrf_token=cookie_token)
r = requests.post("http://192.168.56.102/signin", data=payload, cookies=cookies,headers=user_agent)

payload = {"title": "test" ,"message": "testtest",'csrf_token': token}
cookies = dict(csrf_token=cookie_token,cid=r.cookies["cid"])
r = requests.post("http://192.168.56.102/board", data=payload, cookies=cookies,headers=user_agent)

