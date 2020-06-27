import json
import requests
from flask import Blueprint, request, jsonify, render_template, redirect

from flask_server import NODE_URL, nodePublicKey_path, save_node_publicKey
from cipherOperations import encryptData

app = Blueprint('app', __name__, template_folder='templates')
BASE_URL = "http://" +  NODE_URL  + "/api/v1"

PUBLIC_KEY = 'nodePublicKey.pem'

@app.route("/test")
def test():
    return render_template("DO_NOT_EDIT.html")


@app.route("/pending")
def showPending():
    URL =  BASE_URL + "/get/pendingTransaction"
    print(URL)
    re = requests.get(URL)
    ll = re.json()
    print(ll)
    #show list of pending transaction
    return render_template('pending.html', data=ll)
    

def submit_vote(uid, status):
    data = {}
    trans = {}
    data["uid"]  = encryptData(nodePublicKey_path, uid)
    data["status"]  = encryptData(nodePublicKey_path, str(status))
    response = requests.post(url=BASE_URL + "/clientTranSubmit", json=data)
    response = response.json()
    return response["code"], response["status"]

@app.route("/vote/<uid>", methods = ["GET", "POST"])
def vote(uid):
    print(request.json)
    if request.method == "GET":
        data = {
            "uid" : uid
        }
        return render_template('vote.html', data=data)
    else:
        vote = request.form.get('vote')
        print(vote)
        save_node_publicKey()
        
        code = None
        status = ""
        if vote == "YES":
            code, status = submit_vote(uid, 1)
        else:
            code, status = submit_vote(uid, 0)
        print(status)
        if code == 0:
            return render_template('voteSubmit.html', data = {"status" : "Your vote has been successfully submited."})
        else:
            return render_template('voteSubmit.html', data = {"status" : "An error occurred while submitting your vote."})
        print(code, status)

        return jsonify({"status" : status})

@app.route("/", methods=['GET', 'POST'])
def addTransaction():
    #home page basically add transaction
    #implement both get and post method
    if request.method == 'POST':
        content = request.form
        save_node_publicKey()
        print(content)
        data = {}
        trans = {}
        trans = content
        print(trans)
        data["transaction"]  = encryptData(PUBLIC_KEY, json.dumps(trans))
        try:
            r = requests.post(url=BASE_URL + "/submitTransaction", json=data)
            print(r.json())
        except Exception as e:
            print(e)
        return redirect('/pending')
    else:
        return render_template('addTransaction.html')
    # return "hello"
