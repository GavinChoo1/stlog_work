import requests

url = "http://localhost:8000/reset-password"
payload = {
    "username": "admin",
    "new_password": "newadmin123"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
