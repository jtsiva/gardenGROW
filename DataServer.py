#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
from urlparse import urlparse, parse_qs
import datetime
import time
from sys import argv
from WaterSched import *

class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
            Used by both the GUI and the base station to get data:
            Check through the URL args to see which pieces of data to grab
            Alternatively, if update=1 is passed then send the next 
                watering time
        """
        self._set_headers()
        query_components = parse_qs(urlparse(self.path).query)

        
        print "in GET method"

        returnData = ""

        try:
            spikeID = query_components["id"]
        except KeyError:
            noID = True

        try:
            update = query_components["update"][0]
            print update
            if 1 == int(update):
                """
                    Send data back in json format
                    Returning:
                    {
                        '0': [dur in minutes] -- int
                        '1': [dur in minutes] -- int
                        '2': [dur in minutes] -- int
                        'sleep': [new deep sleep duration in minutes] -- int
                    }

                """
                #get watering data from schedule
                time = [(0,0) for i in xrange(scheduler.numZones)]
                dur = [0 for i in xrange(scheduler.numZones)]
                for i in xrange(scheduler.numZones):
                    time[i] = scheduler.getNextZoneWatering(i)[0]
                    dur[i] = scheduler.getNextZoneWatering(i)[1]
                
                returnData += '{'

                for z in range (scheduler.numZones):
                    now = datetime.datetime.now().time()
                    if (now.hour * 60 + now.minute) + baseStationInterval > (time[z][0] * 60 + time[z][1]):
                        returnData += '\"' + str(z) + '\": ' + str(dur[z]) + ',\n'
                    else:
                        returnData += '\"' + str(z) + '\": 0\n'

                returnData += '\"sleep\": ' + str(baseStationInterval) + '}'
                print returnData

        except KeyError:
            pass

        if not noID:
            try:
                temp = query_components["temp"]
                print "temp request"
                returnData = getData(spikeID, "temp")
            except KeyError:
                pass                

        self.wfile.write(returnData)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print "in POST method"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)
        """
            data to look like:
            {"spikeID" : xbee id (char array),
             "temp" : number,
             "CMS" : number,
             "RMS" : number,
             "light" : number}
            for sensor update
            
            and like:
            {'waterUsed': int}
            for water usage update. The number is the number of pulses counted
        """  

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        print data
        try:

            storeData (str(data["spikeID"]) + "-temp", int(data["temp"]), st)
            storeData (str(data["spikeID"]) + "-CMS", int(data["CMS"]), st)
            storeData (str(data["spikeID"]) + "-RMS", int(data["RMS"]), st)
            storeData (str(data["spikeID"]) + "-light", int(data["light"]), st)

        except KeyError:
            #if the above fails then we must have a water usage update
            storeData ("waterUsed", data["waterUsed"], st)


        scheduler.update()

        return

#may trade out for more sophisticated backend
def storeData (dataLabel, data, timestamp):
    with open ("data/" + str(dataLabel) + ".txt", "a") as f:
            f.write(str(data) + "," + timestamp + '\n');

#may trade out for more sophisticated backend
def getData (spikeID, dataLabel):
    with open("data/" + str(dataType) + ".txt", "r") as f:
        returnData = f.read()

    return returnData


def run(server_class=HTTPServer, handler_class=S, port=80):
    """
        Set up the watering scheduler and then start the server
    """

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Exiting..."

if __name__ == "__main__":
    scheduler = dawnDuskScheduler (numZones = 1)
    scheduler.update()
    baseStationInterval = 10#30 #minutes, can match scheduler

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
