from flask_server import start_server

webhook_functions = {}

# Set the NODE_URL variable to the base url of the blockchain node
NODE_URL = "127.0.0.1:5000"
# Set ip and port to start flask server
ip = "127.0.0.1"
port = "9000"

def getURL():
    return NODE_URL

def setNotifyNewNode(checkNode):
    webhook_functions["NotifyNewNode"] = checkNode
    
def setNotifyNewTransaction(checkTransaction):
    webhook_functions["NotifyNewTransaction"] = checkTransaction

def get_function(name):
    return webhook_functions[name]

def start_flask_server():
    start_server(ip, port, webhook_functions, NODE_URL)