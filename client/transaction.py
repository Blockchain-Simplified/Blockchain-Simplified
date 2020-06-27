import requests, json, time, sys
from cipherOperations import encryptData


API_ENDPOINT = "http://0.0.0.0:{}/api/v1".format(str(sys.argv[1]))

PUBLIC_KEY = 'nodePublicKey.pem'
ll = []
def addTransaction():
    data = {}
    global ll
    trans = {}
    key = str(input("Enter Key : "))
    val = str(input("Enter Value : "))
    trans[key] = val
    data["transaction"]  = encryptData(PUBLIC_KEY, json.dumps(trans))

    r = requests.post(url=API_ENDPOINT + "/submitTransaction", json=data)

    print(r.json())
    r = r.json()
    ll.append(r["uid"])
    return r["uid"]

def voteTransaction(uid):
    data = {}
    data["uid"]  = encryptData(PUBLIC_KEY, uid)
    data["status"]  = encryptData(PUBLIC_KEY, "1")
    r = requests.post(url=API_ENDPOINT + "/clientTranSubmit", json=data)

    print(r.json())

# testCode()
# time.sleep(100)
# testCode1()

while True:
    print("1) Add Transaction\n2) Vote Transaction\n")
    num = int(input("Choice : "))
    if num == 1:
        addTransaction()
    else :
        z = 1
        for i in ll:
            print(z, i)
            z += 1
        index = int(input("Select uid index : "))
        index = index - 1
        voteTransaction(str(ll[index]))

