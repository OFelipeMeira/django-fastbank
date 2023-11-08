# http://127.0.0.1:8000/api/v1/users/1/
import requests
# r = requests.get('http://127.0.0.1:8000/api/v1/users/1/').json()
r = requests.get('http://127.0.0.1:8000/api/v1/users/').json()
# print(r["id"])
print(r)