from configparser import ConfigParser 
import os 


def setUid(uid):
    cp = ConfigParser() 
    try:
        os.remove('config.ini')
    except:
        pass
    cp.add_section("static")
    cp.set("static", "uid", str(uid))
    with open('config.ini', 'w') as configfile:
        cp.write(configfile)

def getUid():
    configure = ConfigParser()
    configure.read('config.ini')
    try:
        uid = configure.get("static", "uid")
        return True, uid
    except:
        return False, 0
