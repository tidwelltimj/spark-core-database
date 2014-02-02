import requests
import time
import json
from pymongo import MongoClient
from datetime import datetime
DBclient = MongoClient() #fill in DB address if other than default
DB = DBclient.temp
temps = DB.temps
access_token ="YOUR TOKEN HERE"
device_id = "YOUR ID HERE"
p = {"access_token":access_token}
url = "https://api.spark.io/v1/devices/"+device_id+"/temp"


while(True):
    
    r = requests.get(url,params=p)   

    datadict = json.loads(r.text)
    try:
        temp = float(datadict[u"result"])

        Now=datetime.now()
        post = {"datetime":Now,"temperature":temp,"location":"desk"}
        print post
        ID = temps.insert(post)
        print ID
        
    except KeyError:
        print "error"
    time.sleep(10)
