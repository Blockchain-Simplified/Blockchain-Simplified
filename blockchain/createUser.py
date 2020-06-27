import requests
from cipherOperations import encryptData

PUBLIC_KEY = "keys/public.pem"

API_ENDPOINT = "http://0.0.0.0:5000/api/v1/createUser"

username = input("Enter username : ")
password = input("Enter password : ")

username = encryptData(PUBLIC_KEY, username)
password = encryptData(PUBLIC_KEY, password)

data ={ 'username' : username,
		'password' : password }

r = requests.post(url=API_ENDPOINT, data=data)

print(r)