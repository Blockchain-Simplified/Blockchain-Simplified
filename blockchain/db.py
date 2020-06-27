from peewee import *
import datetime, hashlib
db = SqliteDatabase('blockchain.db')

PRE_HASH_STR = "0000000"


class BaseModel(Model):
    class Meta:
        database = db

class Chain(BaseModel):
    index = IntegerField(unique=True)
    transaction = TextField() # JSON DATA
    timeStamp = TimestampField(default=datetime.datetime.now)
    preHash = CharField(max_length=5000)
    currHash = CharField(max_length=5000)

class PendingTransaction(BaseModel):
    uid = CharField(max_length=500, unique=True, primary_key=True)
    transaction = TextField() # JSON DATA
    timeStamp = TextField() # Str DATA
    count  = IntegerField(default=0)
    flag = IntegerField(default=0)
    proposingNode = CharField(max_length=500)
    blockindex = IntegerField()

class Clients(BaseModel):
    uid = CharField(max_length=5000, unique=True)
    callback_URL = CharField(max_length=5000)
    publicKey = CharField(max_length=5000)

class Users(BaseModel):
    username = CharField(max_length=5000)
    password = CharField(max_length=5000) # SHA_256_HASH

class Nodes(BaseModel):
    name = CharField(max_length=5000)
    ip = CharField(max_length=5000) # with port and reachable
    publicKey = CharField(max_length=5000)

db.connect()
db.create_tables([Chain, Clients, Nodes, Users, PendingTransaction])

def addData(index, transaction, timeStamp):
    if index == 0:
        get_some_string = str(index) + transaction + str(timeStamp)
        currHash = hashlib.sha256(get_some_string.encode('utf-8')).hexdigest()
        preHash = hashlib.sha256(PRE_HASH_STR.encode('utf-8')).hexdigest()
        print(currHash, preHash)
        Chain.create(index=index, transaction=transaction, timeStamp=timeStamp, preHash=preHash, currHash=currHash)
    else:
        data = retrieve(index-1)
        get_some_string = str(index) + transaction + str(timeStamp)
        currHash = hashlib.sha256(get_some_string.encode('utf-8')).hexdigest()
        preHash = data.currHash
        print(currHash, preHash)
        Chain.create(index=index, transaction=transaction, timeStamp=timeStamp, preHash=preHash, currHash=currHash)

    db.commit()

def getChainDB():
    out = Chain.select()
    import json
    ll = []
    for i in out:
        m = {}
        m["index"] = i.index
        m["transaction"] = json.loads(i.transaction)
        m["timeStamp"] = str(i.timeStamp)
        m["currHash"] = i.currHash
        ll.append(m)
    return ll

def addNodes(name, ip, publicKey):
    if "http://" not in ip:
        ip = "http://" + ip
    Nodes.create(name=name, ip=ip, publicKey=publicKey)
    db.commit()

def addUsers(username, password):
    hashpash = str(hashlib.sha256(password.encode('utf-8')).hexdigest())
    Users.create(username=username, password=hashpash)
    db.commit()

def addClient(uid, callback_URL, publicKey):
    Clients.create(uid=uid, callback_URL=callback_URL, publicKey=publicKey)
    db.commit()

def getAllClients():
    data = []
    names = Clients.select()
    for name in names:
        data.append(name)
    return data

def getLastIndex():
    count = 0
    names = Chain.select()
    for name in names:
        count += 1
    return count

def addPendingTransaction(uid, proposingNode, transaction,  blockindex, timeStamp):
    PendingTransaction.create(uid=uid, proposingNode=proposingNode, transaction=transaction,  blockindex=blockindex, timeStamp=timeStamp, count=0)
    db.commit()

def getPendingTransaction(uid):
    out = PendingTransaction.select().where(PendingTransaction.uid == uid).get()
    return out

def getALLPendingTransaction():
    out = PendingTransaction.select()
    return out

def retrieveNodeList():
    out = Nodes.select()
    return out

def NodeCount():
    out = Nodes.select()
    z = 0
    for i in out:
        z += 1
    return z

def getFlag(uid):
    out = PendingTransaction.select().where(PendingTransaction.uid == uid).get()
    return out.flag

def setFlag(uid, flag):
    out = PendingTransaction.select().where(PendingTransaction.uid == uid).get()
    out.flag = flag
    out.save()
    db.commit()
    return out.flag



def getVoteCount(uid):
    out = PendingTransaction.select().where(PendingTransaction.uid == uid).get()
    return int(out.count)

def setVoteCount(uid, count):
    out = PendingTransaction.select().where(PendingTransaction.uid == uid).get()
    out.count = count
    db.commit()
    out.save()
    return out.count

def retrieve(index):
    try:
        out = Chain.select().where(Chain.index == index).get()
    except: 
        return -1
    return out