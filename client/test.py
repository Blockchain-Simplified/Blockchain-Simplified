import configFileControl
import uuid

def check_and_get_uid():
    status, uid = configFileControl.getUid()
    if status:
        return uid
    else:
        uid = uuid.uuid4()
        configFileControl.setUid(str(uid))
        return uid

uid = check_and_get_uid()
print(uid)