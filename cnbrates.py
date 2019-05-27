import requests

r = requests.get("http://localhost/latest")

print(r.json())