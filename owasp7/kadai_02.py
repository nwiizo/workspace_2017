import requests
from bs4 import BeautifulSoup
import sys

angs = sys.argv

payload = {"username":str(angs[1]),"password":str(angs[2])}
r = requests.post("http://192.168.16.128/WackoPicko/users/login.php",data=payload)

s=BeautifulSoup(r.text,"html.parser")
a_list=s.findAll("h2")

for n in a_list:
       	print(n)

