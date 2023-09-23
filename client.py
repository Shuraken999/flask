import requests

# response = requests.post('http://127.0.0.1:5000/user/',
#                          json={'email': 'user_1@email.org', 'password': '123'},
#
#                          )
# print(response.status_code)
# print(response.json())

# response = requests.get('http://127.0.0.1:5000/user/10000',)
# print(response.status_code)
# print(response.json())

# response = requests.patch('http://127.0.0.1:5000/user/1',
#                           json={'email': 'user_new@email.org', })
# print(response.status_code)
# print(response.json())

response = requests.delete(
    "http://127.0.0.1:5000/user/1",
)
print(response.status_code)
print(response.json())

response = requests.get(
    "http://127.0.0.1:5000/user/1",
)
print(response.status_code)
print(response.json())
