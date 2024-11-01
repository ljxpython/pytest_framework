import requests

body = {
    "username": "test",
    "password": "test",
}
resp = requests.session().post(
    "https://www.coder-ljx.cn:5002/api/user/login", json=body
)
print(resp.json())
