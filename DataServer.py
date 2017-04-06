from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
from urlparse import urlparse, parse_qs
import datetime
import time



class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        query_components = parse_qs(urlparse(self.path).query)

        #check through the URL args to see which pieces of data to grab
        #all data is written to a file named like: spike_#_param.txt
        #the GET message is intended to be used by the client front-end
        #to feed data to GUI
        #NO WRITING
        print "in GET method"

        spikeID = query_components["id"]
        if None != spikeID:
            print "id = " + str(spikeID)

        temp = query_components["temp"] 

        if None != temp:
            print "temp request"
            returnData = getData(spikeID, "temp")
            

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
        # data to look like:
        # {"spikeID" : [0-2],
        #  "temp" : number,
        #  "CMS" : number,
        #  "RMS" : number,
        #  "light" : [0-3]}

        spikeID = data["spikeID"]
        temp = data["temp"]
        cms = data["CMS"]
        rms = data["RMS"]
        light = data["light"]

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        storeData (spikeID, "temp", int(data["temp"]), st)
        storeData (spikeID, "CMS", int(data["CMS"]), st)
        storeData (spikeID, "RMS", int(data["RMS"]), st)
        storeData (spikeID, "light", int(data["light"]), st)

        return

#may trade out for more sophisticated backend
def storeData (spikeID, dataType, data, timestamp):
    with open ("data/spike_" + str(spikeID) +"_" + str(dataType) + ".txt", "a") as f:
            f.write(str(data) + "," + timestamp + '\n');

#may trade out for more sophisticated backend
def getData (spikeID, dataType):
    with open("spike_" + str(spikeID) + "_" + str(dataType) + ".txt") as f:
        returnData = f.read()

    return returnData


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()