from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,\
MinuteLocator, SecondLocator
from numpy import arange
import numpy
client_ip = "" #insert DB ip or leave blank if default
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
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist  
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist2,"-")
        ax.xaxis.set_major_locator(HourLocator(arange(0,24,2)))
        ax.xaxis.set_minor_locator( MinuteLocator(arange(0,60,20)))
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )  
    if window == "12hour":
        twelve_hour_ago = Now-timedelta(hours=12)
        for temp in temps.find({"datetime":{"$gt":twelve_hour_ago}}):
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
    if window == "6hour":
        six_hour_ago = Now-timedelta(hours=6)
        for temp in temps.find({"datetime":{"$gt":six_hour_ago}}):
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
    if window == "hour":
        hour_ago = Now-timedelta(hours=1)
        for temp in temps.find({"datetime":{"$gt":hour_ago}}):
            templist.append(((9.0/5.0)*temp["temperature"])+32)
            datelist.append(temp["datetime"])
        try:
            templist2 = apply_moving_average(templist, w=smoothing)
        except:
            templist2 = templist  
        fig, ax = plt.subplots()
        ax.plot_date(datelist,templist2,"-")
        ax.xaxis.set_major_locator( MinuteLocator(arange(0,60,5)))
        ax.xaxis.set_minor_locator( MinuteLocator())
        ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )
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
    c.close()
    plt.show()
    
    return;
MongoGraph("day",smoothing=20)
