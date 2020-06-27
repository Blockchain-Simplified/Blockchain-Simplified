import uuid

import requests
from flask import Flask, request
from flask import jsonify

import configFileControl
from cipherOperations import genrateKeys, decryptData, saveKeyinFile
# =============================================================================================================================

NODE_URL = ""
BASE_API = "/api/v1"
nodePublicKey_path = 'nodePublicKey.pem'
# =============================================================================================================================
base_url = "/webhook"
private_key_path = 'private.pem'
public_key_path = 'public.pem'
webhook_functions = None
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# =============================================================================================================================

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# =============================================================================================================================


@app.route(base_url, methods = ["GET"])
def home():
    return jsonify({"name" : "Home Test"})

@app.route(base_url + "/addNode", methods = ["POST"])
def check_node():
    data = request.get_json()
    print(data)
    try:
        dataToFunction = {}
        params = ["name", "companyName", "companyID"]
        for i in params:
            dataToFunction[i] = decryptData(private_key_path, data[i])
        print(dataToFunction)
        NotifyNewNode = webhook_functions["NotifyNewNode"]

        name = dataToFunction["name"]
        companyName = dataToFunction["companyName"]
        companyID = dataToFunction["companyID"]

        status = NotifyNewNode(name, companyName, companyID)
        print(status)
        if status == True:
            return jsonify({"code": 0, "status": "Node added"})
        else:
            return jsonify({"code": 1, "status": "Something Went Wrong"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})

@app.route(base_url + "/addTransaction", methods = ["POST"])
def check_transaction():
    data = request.get_json()
    print(data)
    try:
        dataToFunction = {}
        params = ["proposingNode", "transaction", "blockindex", "uid"]
        for i in params:
            dataToFunction[i] = decryptData(private_key_path, data[i])
        print(dataToFunction)
        NotifyNewTransaction = webhook_functions["NotifyNewTransaction"]

        proposingNode = dataToFunction["proposingNode"]
        transaction = dataToFunction["transaction"]
        blockindex = dataToFunction["blockindex"]
        uid = dataToFunction["uid"]

        status = NotifyNewTransaction(proposingNode, transaction, blockindex, uid)
        print(status)
        if status == True:
            return jsonify({"code": 0, "status": "Transaction added"})
        else:
            return jsonify({"code": 1, "status": "Something Went Wrong"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})
# =============================================================================================================================

def register_client(uid, ip, port):
    publicKey = None
    with open('public.pem', 'r') as f:
        publicKey = f.read()
    payload = {
        "uid" : uid,
        "publicKey" : publicKey,
        "ipaddr" : ip + ":" + port
    }
    response = requests.post("http://" + NODE_URL + "/registerClient", json=payload)
    response = response.json()
    return response["code"]

def save_node_publicKey():
    response = requests.get("http://" + NODE_URL + BASE_API + "/check")
    response = response.json()
    print(response)
    saveKeyinFile(nodePublicKey_path, response["publicKey"])

def check_client(uid, ip, port):

    payload = {
        "uid" : uid
    }
    response = requests.post("http://" + NODE_URL + "/checkClient", json=payload)
    response = response.json()
    # code 1 means client is not registered
    if response["code"] == 1:
        code = register_client(uid, ip, port)
        if code == 0:
            print("Client Registered")
            # calling node api to retrieve node public key and save it
            save_node_publicKey()
            return True
        else:
            print("An error occured while registering client")
            return False
    else:
        print(response["status"])
        return True

def check_and_get_uid():
    status, uid = configFileControl.getUid()
    if status:
        return uid
    else:
        uid = uuid.uuid4()
        configFileControl.setUid(uid)
        return uid



def start_server(ip, port, webhook_functions_arg, node_url):
    genrateKeys(private_key_path, public_key_path)

    global webhook_functions, NODE_URL
    webhook_functions = webhook_functions_arg
    NODE_URL = node_url
    from ui import app as clienAPPT
    global app
    app.register_blueprint(clienAPPT)
    uid = str(check_and_get_uid())
    status = check_client(uid, ip, port)
    if status:
        app.run(host=ip, port=port, debug=True)
    