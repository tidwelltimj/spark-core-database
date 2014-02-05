spark-core-database
===================
simple set of applications to collect, store and display temperature data using a Spark core and MongoDB

Setup:

copy and paste the firmware file into the web IDE and flash the core.

next setup mongodb, following instructions at http://www.mongodb.org/  

the script for pinging the spark core uses python and the required dependencies are requests, pyMongo and MatLibPlot.

mongograph.py is a very basic script to collect the data from the database and graph it. It's very much in a beta stage but the hope is to eventually be able to load the graphs through a web browser


webserver.py is a tornado based sever to display graphs of the data in the mongoDB.  It is currently set up to run in a linux environment but can be ran on windows with small changes to the directory settings

