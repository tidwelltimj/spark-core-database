import tornado.ioloop
import tornado.web
import tornado
import os
import json, requests
import matplotlib
matplotlib.use("Agg")
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,\
MinuteLocator, SecondLocator
from numpy import arange
STATIC_PATH= os.path.join(os.path.dirname(__file__),r"static/")
global _window
_window ="12hour"
client_ip = "insert mongoDB IP address here" #can leave untouched if mongoDB is on same host
def apply_moving_average(List,w=5):
    """
    givien a list of numbers, applies a simple moving average with a window of w
    """
    Window = int(w) #window of average
    if Window %2 ==0:
        Window +=1
    spread = Window/2 # +- on each side
    try:
        new_list=[0 for i in range(len(List))]
        for i in range(0,spread):
            new_list[i]=List[i]
            
        for j in range(spread,len(List)-spread):
            c=spread
            Sum = List[j]
            while c>0:
                Sum +=List[j-c]
                Sum +=List[j+c]
                c-=1
            new_list[j]=Sum/float(Window)
        for i in range(len(List)-spread,len(List)):
            new_list[i]=List[i]
        return new_list
    except:
        return List      
     
def MongoGraph(window,smoothing="off"): 
    """
    window options are day 12Hour, 6Hour, Hour, 30min,5min. \
smoothing sets the window of a simple moving average
    """
    try:
        c = MongoClient(client_ip)
    except:
        c = MongoClient()
    db = c.temp
    temps = db.temps
    templist=[]
    datelist=[]
    Now = datetime.now()
    if window == "day":
        day_ago = Now-timedelta(hours=24)
        for temp in temps.find({"datetime":{"$gt":day_ago}}):
            if temp[u"temperature"] >100:
                continue
            
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
            doc = {"datetime":temp[u"datetime"],"temperature":temp[u"temperature"]}
            
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist  
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist2,"-")
        ax.xaxis.set_major_locator(HourLocator(arange(0,24,2)))
        ax.xaxis.set_minor_locator( MinuteLocator(arange(0,60,20)))
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )  
    elif window == "12hour":
        twelve_hour_ago = Now-timedelta(hours=12)
        for temp in temps.find({"datetime":{"$gt":twelve_hour_ago}}):
            if temp[u"temperature"] >100:
                continue            
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist  
        fig, ax = plt.subplots()
        
        ax.plot_date(datelist,templist2,"-")
        ax.set_xlabel('Date')
        ax.xaxis.set_major_locator(HourLocator())
        ax.xaxis.set_minor_locator( MinuteLocator(arange(0,60,10)))
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )  
	ax.autoscale_view()
	fig.autofmt_xdate()
	plt.autoscale()      
    elif window == "6hour":
        six_hour_ago = Now-timedelta(hours=6)
        for temp in temps.find({"datetime":{"$gt":six_hour_ago}}):
            if temp[u"temperature"] >100:
                continue
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist  
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist2,"-")
        ax.xaxis.set_major_locator(HourLocator())
        ax.xaxis.set_minor_locator( MinuteLocator(arange(0,60,10)))
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )    
    elif window == "hour":
        
        hour_ago = Now-timedelta(hours=1)
        for temp in temps.find({"datetime":{"$gt":hour_ago}}):
            if temp[u"temperature"] >100:
                continue
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist
        
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist2,"-")
        ax.set_xlabel('Date')
        ax.xaxis.set_major_locator( MinuteLocator(arange(0,60,5)))
        ax.xaxis.set_minor_locator( MinuteLocator())
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )  
	ax.autoscale_view()
	fig.autofmt_xdate()
	plt.autoscale()     
	
    elif window =="30min":
        thirty_min_ago = Now-timedelta(minutes=30)
        for temp in temps.find({"datetime":{"$gt":thirty_min_ago}}):
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])            
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist,"-")
        ax.xaxis.set_major_locator( MinuteLocator(arange(0,60,10)))
        ax.xaxis.set_minor_locator( MinuteLocator())
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )
    elif window =="5min":
        five_min_ago = Now-timedelta(minutes=5)
        for temp in temps.find({"datetime":{"$gt":five_min_ago}}):
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])            
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist,"-")
        ax.xaxis.set_major_locator( MinuteLocator())
        ax.xaxis.set_minor_locator(SecondLocator(arange(0,60,10)))
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M') )
	ax.autoscale_view()
	ax.grid(True)

	fig.autofmt_xdate()
	
    c.close()
    f = open("static/graph.svg","w")
    plt.autoscale()
    plt.savefig(f,format="svg")   
         
    f.close()
    
    return;


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("login")
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        try:
            MongoGraph(_window,smoothing=11)
        except:
            try:
                MongoGraph("day",smoothing=11)
            except:
                pass
      
	self.render("index.html", number=_window,image=x) 
	print _window   
    def post(self):
        Input = self.request
        arg = Input.arguments
        arg["time"]=datetime.now()
        try:
            global _window
            _window=arg["name"][0]  				
        except:
            pass
        self.redirect("/")

class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")
	def post(self):
		password = self.get_argument("password")
		if password == "1234":
			self.set_secure_cookie("login","23",expires_days=5)
			self.redirect("/")
		else:
			self.write("wrong password")
			self.set_status(404)
		
application = tornado.web.Application([
	(r"/", MainHandler),	
	(r"/login/", LoginHandler),
],debug=True,static_path=STATIC_PATH,login_url=r"/login/",cookie_secret="35wfaa35tgty5wf5yhxbt4")

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()