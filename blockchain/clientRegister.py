from flask import Blueprint, request, jsonify
from dateutil import parser
app = Blueprint('app', __name__, template_folder='templates')
import requests
from db import addClient, getAllClients, getVoteCount, retrieveNodeList, setVoteCount, NodeCount, setFlag, getFlag, addData, getLastIndex, getPendingTransaction, getChainDB, getALLPendingTransaction
PRIVATE_KEY = "keys/private.pem"
PUBLIC_KEY = "keys/public.pem"
BASE_API = "/api/v1"
from cipherOperations import encryptData, decryptData, saveKeyinFile
@app.route('/checkClient', methods=['POST'])
def checkClient():
    content = request.json
    uid = content["uid"]
    ll = getAllClients()
    for i in ll:
        if i.uid == uid:
            return jsonify({"code": 0, "status": "Go Ahead"})
    return jsonify({"code": 1, "status": "Something went wrong"})

@app.route('/registerClient', methods=['POST'])
def registerClient():
    content = request.json
    uid = content["uid"]
    publicKey = content["publicKey"]
    address = content["ipaddr"]
    try:
        addClient(uid, "http://" + str(address) + "/webhook", publicKey)
        # print(getAllClients())
        return jsonify({"code": 0, "status": "Client Register"})
    except:
        return jsonify({"code": 1, "status": "Someting Went Wrong"})


def calScore(uid):
    nodes = NodeCount()
    score = getVoteCount(uid)
    print(nodes, score, "nn")
    if int(score) >= int(nodes):
        return True
    return False

def addToBlockChain(uid):
    pendT = getPendingTransaction(uid)
    addData(getLastIndex(), pendT.transaction, parser.parse(pendT.timeStamp))
    return setFlag(uid, "1")


@app.route(BASE_API + '/nodeTranSubmit', methods=['POST'])
def nodeTranSubmit():
    content = request.json
    try :
        uid = decryptData(PRIVATE_KEY, content['uid'])
        status = decryptData(PRIVATE_KEY, content['status'])
        if status == "1":
            setVoteCount(uid, getVoteCount(uid) + 1)
        if calScore(uid) == True and str(getFlag(uid)) == "0":
            addToBlockChain(uid)
        return jsonify({"code": 0, "status": "OK Got IT"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})


@app.route(BASE_API + '/clientTranSubmit', methods=['POST'])
def clientTranSubmit():
    content = request.json
    try :
        uid = decryptData(PRIVATE_KEY, content['uid'])
        status = decryptData(PRIVATE_KEY, content['status'])
        if status == "1":
            setVoteCount(uid, getVoteCount(uid) + 1)
        if calScore(uid) == True and str(getFlag(uid)) == "0":
            addToBlockChain(uid)

        #call others here
        ll = retrieveNodeList()
        for i in ll:
            try:
                TEMP_KEY = "keys/tempKey.pem"
                saveKeyinFile(TEMP_KEY ,i.publicKey)
                data = {}
                data["uid"] = encryptData(TEMP_KEY, uid)
                data["status"] = encryptData(TEMP_KEY, status)
                rr = requests.post(i.ip + BASE_API + '/nodeTranSubmit', json=data)
            except Exception as e:
                print(e)
        return jsonify({"code": 0, "status": "OK Got IT"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})


@app.route("/blockchain", methods=["GET"])
def getChain():
    try:
        ll = getChainDB()
        out = {}
        out["code"] = 0
        out["status"] = "status"
        out["chain"] = ll
        # print(ll)
        return jsonify(out)
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})

@app.route(BASE_API + "/get/pendingTransaction", methods=["GET"])
def getpendingTransaction():
    ll = getALLPendingTransaction()
    import json
    outll = []
    z = 1
    for i in ll:
        if i.flag == 0:
            out = {}
            out["id"] = z
            out["uid"] = i.uid
            out["transaction"] = json.dumps(json.loads(i.transaction), indent=4)
            out["proposingNode"] = i.proposingNode
            z = z + 1
            outll.append(out)
    return jsonify(outll)