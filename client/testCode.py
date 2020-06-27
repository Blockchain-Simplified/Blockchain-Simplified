import requests, json, time
from cipherOperations import encryptData


API_ENDPOINT = "http://0.0.0.0:5000/api/v1"

PUBLIC_KEY = 'nodePublicKey.pem'

def testCode():
    data = {}
    trans = {}
    trans["name"] = "amey"
    data["transaction"]  = encryptData(PUBLIC_KEY, json.dumps(trans))

    r = requests.post(url=API_ENDPOINT + "/submitTransaction", json=data)

    print(r.json())

def testCode1(uid):
    data = {}
    trans = {}
    trans["name"] = "amey"
    data["uid"]  = encryptData(PUBLIC_KEY, uid)
    data["status"]  = encryptData(PUBLIC_KEY, "1")
    r = requests.post(url=API_ENDPOINT + "/clientTranSubmit", json=data)

    print(r.json())
# 1 is yes
#testCode()
# time.sleep(100)
testCode1("3b859b52-8896-4bc6-9f04-aa8a96bf43f6")