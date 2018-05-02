#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import MySQLdb
from generate_data import generate
from SVM import svm
hostname = 'localhost'
username = 'root'
password = '4205'
database = 'dagon'
filename = '/home/capk/FYP/server/myserver/Data/hashes.txt'
fileout =  '/home/capk/FYP/server/myserver/Data/result.txt'
filepermission = '/home/capk/FYP/server/myserver/Data/permission.txt'
filepermissionresult =  '/home/capk/FYP/server/myserver/Data/permission-data.txt'
class S(BaseHTTPRequestHandler):
    global db_request
    def db_request():
	conn = MySQLdb.connect(hostname,username,password,database)
    	cursor = conn.cursor()
	out = open(fileout,"w")
    	with open(filename) as f:
    	    data = f.readlines()
	for d in data:
		out.write(d)
		out.write("\n")
    	for d in data:
    	    	d = d.strip()
		d = d.replace("\n","")
		print d
#    	    	print "SELECT PackageName from DexSignatures where ClassOneHash = '"+d+"'"
       	    	cursor.execute("SELECT PackageName from DexSignatures where ClassOneHash = '"+d+"'")
        	result = cursor.fetchone()
		if (result==None):
			out.write("clean")
			out.write("\n")
		else:
			out.write("infected")
			out.write("\n")
        	print result
    	conn.close()
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
	hash = open("/home/capk/FYP/server/myserver/Data/hashes.txt","w")
        permfile = open(filepermission,"w")
	content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

	post_data = post_data.replace('=','\n',1)
        post_data = post_data.replace('%0A','\n')
        post_data = post_data.replace('%2F','/')
        post_data = post_data.replace('%3D','=')
	post_data = post_data.replace('%2B','+')
        post_data = post_data.replace('&','\n')
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
	if "permissions" in post_data:
		hashes,permissions = post_data.split("permissions")
		hashes = hashes.replace("hashes=",'')
		hash.write(hashes)
		packageName = hashes.split("\n")
		permfile.write(packageName[0])
		permfile.write("\n")
		permissions = permissions.replace("=",'')
		permissions = permissions.replace("%2C",',')
		permfile.write(permissions)
		permfile.close()
		generate()
		svm()
	else:
		hash.write(post_data)
	hash.close()
	db_request()
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
	run()
