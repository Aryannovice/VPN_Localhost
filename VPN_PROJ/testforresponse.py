import requests

url = "http://localhost:8080"
data = "Test Data"

response = requests.post(url, data=data)
print(response.text)
