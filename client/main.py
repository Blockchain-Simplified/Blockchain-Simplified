from webhook import setNotifyNewNode, start_flask_server, setNotifyNewTransaction

def testFunction():
    print("Function as parameter testing")


def checkNewNode(name, companyName, companyID):
    print(companyID, companyName, name)
    if name == "TestNode":
        return True
    else:
        return False

def checkNewTransaction(proposingNode, transaction, blockindex, uid):
    print(uid, transaction)
    if proposingNode == "TestNode":
        return True
    else:
        return False

setNotifyNewNode(checkNewNode)
setNotifyNewTransaction(checkNewTransaction)

start_flask_server()