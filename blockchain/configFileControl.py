from configparser import ConfigParser 
import os 

def setupFile():
    cp = ConfigParser() 
    try:
        os.remove('config.ini')
    except:
        pass
    cp.add_section("static")
    cp.set("static","init","0")
    with open('config.ini', 'w') as configfile:
        cp.write(configfile)

def getInit():
    configure = ConfigParser() 
    configure.read('config.ini')
    return configure.get("static", "init")

def getName():
    configure = ConfigParser() 
    configure.read('config.ini')
    return str(configure.get("static", "name"))

def setInit():
    configure = ConfigParser() 
    configure.read('config.ini')
    configure.set("static", "init", "1")
    saveData(configure)


def setName(name):
    configure = ConfigParser() 
    configure.read('config.ini')
    configure.set("static", "name", name)
    saveData(configure)
    

def saveData(configure):
    with open('config.ini', 'w') as configfile:
        configure.write(configfile)

def setBlockChain(name, ipaddr, info):
    configure = ConfigParser() 
    configure.read('config.ini')
    configure.set("static", "name", name)
    configure.set("static", "ipaddr", ipaddr)
    configure.set("static", "info", info)
    saveData(configure)


def getTrasactionData():
    configure = ConfigParser() 
    configure.read('config.ini')
    return configure.get("static", "name")  , configure.get("static", "index") 

setupFile()

