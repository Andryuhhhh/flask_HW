import requests

response = requests.post(
    "http://127.0.0.1:5000/users",
    json={"name": "user_5", "password": "ssfefe34vfgbfbfsf"},
)

print(response.status_code)
print(response.json())


# response = requests.get("http://127.0.0.1:5000/users/7")
# print(response.status_code)
# print(response.json())


# response = requests.patch("http://127.0.0.1:5000/users/7",
#                           json={"name": "new_user_name_2"})
# print(response.status_code)
# print(response.json())


# response = requests.get("http://127.0.0.1:5000/users/7")
# print(response.status_code)
# print(response.json())

# response = requests.delete("http://127.0.0.1:5000/users/7")
# print(response.status_code)
# print(response.json())

# response = requests.get("http://127.0.0.1:5000/users/7")
# print(response.status_code)
# print(response.json())
