import requests
payload = {"username":"scanner1","password":"scanner1"}
r = requests.post("http://192.168.16.128/WackoPicko/users/login.php",data=payload)
print(r.text)


