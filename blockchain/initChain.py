from db import addData
import json, datetime

for i in range (0, 100):
    data ={}
    timeStamp = datetime.datetime.now()
    data["name"] = "Amey" + str(i)
    addData(i, json.dumps(data), timeStamp)