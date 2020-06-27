from flask import Flask, render_template, Response, request, jsonify, send_file
from db import addUsers, addPendingTransaction, addNodes, getAllClients, getLastIndex, retrieveNodeList
import uuid, requests, datetime
from configFileControl import getInit, setName, setBlockChain, getTrasactionData, getName, setInit
from cipherOperations import genrateKeys, decryptData, encryptData, saveKeyinFile
app = Flask(__name__)
from clientRegister import app as clienAPPT
from cipherOperations import encryptData, decryptData
app.register_blueprint(clienAPPT)
import sys
import json
from werkzeug.utils import secure_filename

PRIVATE_KEY = "keys/private.pem"
PUBLIC_KEY = "keys/public.pem"

BASE_API = "/api/v1"

URL = "http://0.0.0.0:"+str(sys.argv[1])

try:
    import os
    os.mkdir("keys")
except:
    pass

#setup uri
@app.route('/')
def index():
    val = getInit()
    if int(val) == 0:
        return render_template('index.html')
    else:
        return render_template('initDone.html')

@app.route('/create', methods=['POST'])
def create():
    # print("here")
    content = request.form
    print(content)
    rr = requests.post(URL + BASE_API + '/createUser', json=content)
    print(rr.json())
    return render_template('create.html')

@app.route('/join', methods=['POST'])
def join():
    content = request.form
    rr = requests.post(URL + BASE_API + '/createUser', json=content)
    print(rr.json())
    
    return render_template('join.html')

@app.route(BASE_API + '/check', methods=['GET'])
def checkInit():
    val = getInit()
    print(val)
    if int(val) == 1:
        nodePublicKey = str(open(PUBLIC_KEY, 'r').read())
        return jsonify({"code": 1, "status" : "Already Init", "publicKey" : nodePublicKey})
    else:
        genrateKeys(PRIVATE_KEY, PUBLIC_KEY)
        nodePublicKey = str(open(PUBLIC_KEY, 'r').read())
        return jsonify({"code": 0, "status" : "GO Ahead", "publicKey" : nodePublicKey})

@app.route(BASE_API + '/createUser', methods=['POST'])
def createUser():
    content = request.json
    try:
        # setName(decryptData(PRIVATE_KEY, content['name']))
        # username = decryptData(PRIVATE_KEY, content["username"])	
        # password = decryptData(PRIVATE_KEY, content["password"])

        username = content["username"]
        password = content["password"]
        addUsers(username, password)
        checkInit()
        return jsonify({"code": 0, "status": "User Created"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})

@app.route(BASE_API + "/createBlockchain", methods=['POST'])
def createBlockchain():
    content = request.form
    print(content["name"])
    try:
        print("here")
        # name = decryptData(PRIVATE_KEY, content["name"])
        # nodeName = decryptData(PRIVATE_KEY, content["nodeName"])
        # ipaddr = decryptData(PRIVATE_KEY, content["ipaddr"])
        # info = decryptData(PRIVATE_KEY, content["info"])
        
        name = content["name"]
        nodeName = content["nodeName"]
        ipaddr = content["ipaddr"]
        info = content["info"]
        setBlockChain(nodeName, ipaddr, info)
        print("here2")
        blockchain = {}
        node = {}
        ll= []
        node["name"] = nodeName
        node["ipaddr"] = ipaddr
        node['publicKey'] = open(PUBLIC_KEY, 'r').read()
        blockchain['name'] = name
        ll.append(node)
        blockchain['nodes'] = ll
        blockchain['info'] = info
        data = {}
        data["code"] = 0
        data["status"] = "Blockchain Created"
        data["blockchain"] = blockchain
        print(type(data["blockchain"]))
        print(data)
        with open('blockchainCard.json', 'w') as outfile:
            try:
                json.dump(data["blockchain"], outfile, indent=2)
            except Exception as e:
                print(e)
        try:
            setInit()
            return send_file('blockchainCard.json', as_attachment=True)
        except Exception as e:
            return str(e)
    except:
        return jsonify({"code": 1, "status": "Something Went Wrong"})

@app.route(BASE_API + "/joinBlockchain", methods=['POST'])
def joinBlockchain():
    content = request.form
    f = request.files['file']
    f.save(secure_filename(f.filename))
    json_data  = open(f.filename, 'r').read()
    # json_data = json.dumps(json_data)
    json_data = eval(json_data)
    print(type(json_data))
    try:
        print(content)
        nodes = json_data['nodes']
        print(nodes)
        # new_content = content["new_node_data"]
        # name = decryptData(PRIVATE_KEY, new_content['name'])
        # ipaddr = decryptData(PRIVATE_KEY, new_content['ipaddr'])
        # info = decryptData(PRIVATE_KEY, new_content['info'])
        # companyName = decryptData(PRIVATE_KEY, new_content['companyName'])
        # companyID = decryptData(PRIVATE_KEY, new_content['companyID'])
        name = content["name"]
        ipaddr = content["ipaddr"]
        info = content["info"]
        companyName = content["companyName"]
        companyID = content["companyID"]

        publicKey = str(open(PUBLIC_KEY, 'r').read())
        setBlockChain(name, ipaddr, info)
        print(nodes)
        z = 0
        for i in nodes:
            TEMP_KEY = "keys/tempKey.pem"
            saveKeyinFile(TEMP_KEY , i["publicKey"])
            data = {}
            addNodes(i["name"], i["ipaddr"], i["publicKey"])
            z = z + 1
            data["name"] = encryptData(TEMP_KEY, name)
            data["ipaddr"] = encryptData(TEMP_KEY, ipaddr)
            data["publicKey"] = publicKey
            data["companyName"] = encryptData(TEMP_KEY, companyName)
            data["companyID"] = encryptData(TEMP_KEY, companyID)
            URL = "http://" + str(i["ipaddr"]) + BASE_API + "/nodeRequest"
            print(URL)
            try:
                rr = requests.post(URL, json=data)
                print(rr.json())
            except Exception as e:
                print(e)
        setInit()
        return jsonify({"code": 0, "status": "Joined to blockchain"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})

@app.route(BASE_API + '/nodeRequest', methods=['POST'])
def addNodeRequest():
    content = request.json
    try:
        print("in request")
        name = decryptData(PRIVATE_KEY, content['name'])
        ipaddr = decryptData(PRIVATE_KEY, content['ipaddr'])
        publicKey = content['publicKey']
        companyName = decryptData(PRIVATE_KEY, content['companyName'])
        companyID = decryptData(PRIVATE_KEY, content['companyID'])
        #verify if the node doesn't exist?
        addNodes(name, ipaddr, publicKey)
        ll = getAllClients()
        for i in ll:
            try:
                TEMP_KEY = "keys/tempKey.pem"
                saveKeyinFile(TEMP_KEY, i.publicKey)
                data = {}
                data["name"] = encryptData(TEMP_KEY, name)
                data["companyName"] = encryptData(TEMP_KEY, companyName)
                data["companyID"] = encryptData(TEMP_KEY, companyID)
                try:
                    rr = requests.post(i.callback_URL + '/addNode', json=data)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
        return jsonify({"code": 0, "status": "Node added"})
    except:
        return jsonify({"code": 1, "status": "Something Went Wrong here"})

#External Access uri 
@app.route(BASE_API + "/getTransaction", methods=['POST'])
def getTransaction():
    content = request.json
    try :
        proposingNode = decryptData(PRIVATE_KEY, content['proposingNode'])
        transaction = decryptData(PRIVATE_KEY, content['transaction'])
        blockindex = decryptData(PRIVATE_KEY, content['blockindex'])
        timeStamp = decryptData(PRIVATE_KEY, content['timeStamp'])
        uid = decryptData(PRIVATE_KEY, content['uid'])
        addPendingTransaction(uid, proposingNode, transaction, blockindex, timeStamp)
        #call client for transaction strucutre check
        ll = getAllClients()
        for i in ll:
            try:
                TEMP_KEY = "keys/tempKey.pem"
                saveKeyinFile(TEMP_KEY , i.publicKey)
                data = {}
                data["transaction"] = encryptData(TEMP_KEY, transaction)
                data["proposingNode"] = encryptData(TEMP_KEY, proposingNode)
                data["blockindex"] = encryptData(TEMP_KEY, blockindex)
                data["uid"] = encryptData(TEMP_KEY, uid)
                rr = requests.post(i.callback_URL + '/addTransaction', json=data)
            except Exception as e:
                print(e)
        ##
        #save in pending db
        
        #call client for verify
        return jsonify({"code": 0, "status": "Transaction is submitted to client"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})



#client REST API uri

@app.route(BASE_API + "/submitTransaction", methods=['POST'])
def submitTransaction():
    content = request.json
    try :
        transaction = decryptData(PRIVATE_KEY, content['transaction'])
        proposingNode = getName()
        blockindex = getLastIndex()
        timeStamp = str(datetime.datetime.now())
        uid = str(uuid.uuid4())
        addPendingTransaction(uid, proposingNode, transaction, blockindex, timeStamp)
        ll = retrieveNodeList()
        for i in ll:
            try:
                TEMP_KEY = "keys/tempKey.pem"
                saveKeyinFile(TEMP_KEY ,i.publicKey)
                data = {}
                data["transaction"] = encryptData(TEMP_KEY, transaction)
                data["proposingNode"] = encryptData(TEMP_KEY, proposingNode)
                data["blockindex"] = encryptData(TEMP_KEY, blockindex)
                data["timeStamp"] = encryptData(TEMP_KEY, timeStamp)
                data["uid"] = encryptData(TEMP_KEY, uid)
                rr = requests.post(i.ip + BASE_API + '/getTransaction', json=data)
            except Exception as e:
                print(e)
        return jsonify({"code": 0, "status": "Transaction is submitted to client", "uid" : uid})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "status": "Something Went Wrong"})


if __name__ == '__main__':
    import sys
    app.run(host='0.0.0.0', port=sys.argv[1], threaded=True, debug=True)