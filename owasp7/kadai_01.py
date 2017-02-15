import requests
from bs4 import BeautifulSoup

payload = {"username":"scanner1","password":"scanner1"}
r = requests.post("http://192.168.16.128/WackoPicko/users/login.php",data=payload)

s=BeautifulSoup(r.text,"html.parser")
a_list=s.findAll("h2")

for n in a_list:
       	print(n)

