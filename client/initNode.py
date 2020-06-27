import requests, sys
from cipherOperations import encryptData, saveKeyinFile
import getpass, json
#init node scripts

PUBLIC_KEY = "publicKey.pem"
port = str(sys.argv[1])
BASE_URL = "http://0.0.0.0:{}/api/v1/".format(port)

def checkInit():
    rr = requests.get(BASE_URL + "check")
    data = rr.json()
    saveKeyinFile(PUBLIC_KEY, data['publicKey'])
    return data['code']

def setCredential():
    data = {}
    # data['name'] = encryptData(PUBLIC_KEY, input("Set A Name To Node : "))
    data['username'] = encryptData(PUBLIC_KEY, input("Set username : "))
    data['password'] = getpass.getpass("Set password : ")
    cpassword = getpass.getpass("confirm password : ")
    if data['password'] == cpassword:
        data['password'] = encryptData(PUBLIC_KEY, data['password'])
        newR = requests.post(BASE_URL + "createUser", json=data)
        print(newR.json())
    else:
        print("Password Mismatch try again")
    
def setBlockChain():
    new = input("1. Set a new Blockchain\n2. Join Existing\n")
    if str(new) == "1":        
        data = {}
        data['nodeName'] = encryptData(PUBLIC_KEY, input("Set A Name To Node : "))
        data['name'] = encryptData(PUBLIC_KEY, input("Set A Name To BlockChain : "))
        data['ipaddr'] = encryptData(PUBLIC_KEY, input("IPAddr With Port : "))
        data['info'] = encryptData(PUBLIC_KEY, input("Info about Blockchain : "))
        data["companyName"] = encryptData(PUBLIC_KEY, input("Enter Company name : "))
        data["companyID"] = encryptData(PUBLIC_KEY, input("Enter Company ID : "))    
        try :
            rr = requests.post(BASE_URL + 'createBlockchain', json=data)
            val = rr.json()
            with open('blockchainCard.json', 'w') as outfile:
                json.dump(val['blockchain'], outfile, indent=2)
            # print(rr.json())
        except:
            print("something went wrong")
    elif str(new) == "2":
        path = input("Enter full path to the blockchain.json file : ")
        json_data = {}
        json_data  = json.loads(open(path, 'r').read())
        data = {}
        data["name"] = encryptData(PUBLIC_KEY, input("Enter name for node : "))
        data["ipaddr"] = encryptData(PUBLIC_KEY, input("Enter node's IP address : "))
        data["companyName"] = encryptData(PUBLIC_KEY, input("Enter Company name : "))
        data["companyID"] = encryptData(PUBLIC_KEY, input("Enter Company ID : "))    
        data['info'] = encryptData(PUBLIC_KEY, input("Info about Blockchain : "))
        json_data["new_node_data"] = data
        print(json_data)
        try:
            rr = requests.post(BASE_URL + 'joinBlockchain', json=json_data)
            val = rr.json()
        except:
            print("something went wrong") 
        # no_of_nodes = json_data['number_of_nodes']
        # for i in range (1, no_of_nodes):
        #     #send request to ipaddr in node+str(i)
        # data = {}
        # data['name'] = encryptData(PUBLIC_KEY, input("Enter name for node : "))
        # data['ipaddr'] = encryptData(PUBLIC_KEY, input("Enter node's IP address : "))
        # data['publicKey'] = encryptData(PUBLIC_KEY, open(PUBLIC_KEY, 'r').read())
        # data['companyName'] = encryptData(PUBLIC_KEY, input("Enter Company name : "))
        # data['companyID'] = encryptData(PUBLIC_KEY, input("Enter Company ID : "))
        # try:
        #     rr = requests.post(BASE_URL + 'nodeRequest', json=data)
        #     val = rr.json()
        #     #add this node if request is completed
        # except:
        #     print("something went wrong")

def main():
    try :
        if checkInit() == 0:
            setCredential()
            setBlockChain()
        else:
            print("Already Init")
    except Exception as e:
        print("Node is not up or check BASE_URL" + str(e))

main()