import requests
import time
import json
from pymongo import MongoClient
from datetime import datetime

access_token ="PASTE ACCESS TOKEN HERE"
device_id = "PASTE DEVICE ID HERE"
p = {"access_token":access_token}
url = "https://api.spark.io/v1/devices/"+device_id+"/temp"


while(True):
    try:
        DBclient = MongoClient() #fill in DB address if other than default
        DB = DBclient.temp
        temps = DB.temps
    except:
	print "can not connect to DB make sure MongoDB is running"
        continue
    try:
	r = requests.get(url,params=p)   
    except:
	print "request failed, check internet connection"
	continue
		
    datadict = json.loads(r.text)
    try:
        temp = float(datadict[u"result"])

        Now=datetime.now()
        post = {"datetime":Now,"temperature":temp,"location":"desk"}
        print post
        ID = temps.insert(post)
        print ID
        
    except KeyError:
        print "error: spark data is invalid or core is not connected"
    DBclient.close()
    time.sleep(10)
