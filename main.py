from http.server import BaseHTTPRequestHandler, HTTPServer # python3
import os
from os.path import join
import subprocess
from glob import glob
'''from flask import Flask
from flask import request'''
import mimetypes
#app = Flask(__name__)
dp = 50
minrng = 0.5
maxrng = 0.05
#@app.route("/")
class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        try:
            print(1,self.path)
            if self.path == "/":
                self.path="/index.html"
            if self.path == "/cart.html":
                fucntions = "functions.py"
                print("cart")
                subprocess.call(['python', os.getcwd()+"/"+fucntions,str(dp),str(minrng),str(maxrng)])
            if '?' in self.path:
                self.path=self.path.replace('?','')
            filepath = join(join(os.getcwd(),'public'),self.path[1:])
            
            print(2,filepath)
            f = open(filepath,"rb")
        except IOError:
            self.send_error(404,'File Not Found: %s ' % filepath)

        else:
            self.send_response(200)
            mimetype, _ = mimetypes.guess_type(filepath)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            for s in f:
                self.wfile.write(s)
    
    #@app.route("/post", methods=['POST'])    
    def do_POST(self):
        self._set_headers()
        content_len = int( self.headers.get('content-length', 0))
        r = self.rfile.read(content_len)
        post_body = r.decode().split("&")
        parsed_pbody = dict()
        
        for post_att in post_body:
            spl = post_att.split("=")
            parsed_pbody[spl[0]]=spl[1]
        print(parsed_pbody)

        if 'id' in parsed_pbody.keys(): #login session
            print("User ID :",parsed_pbody['id'])
            print("User PW :",parsed_pbody['password'])

        if 'stock_name'in parsed_pbody.keys(): #cart purchase session
            en = parsed_pbody['stock_name']
            print('Stock Name:',parsed_pbody['stock_name'])

        if 'days'in parsed_pbody.keys(): #settings parameter session
            print('Number of Days:',parsed_pbody['days'] )
            dp = parsed_pbody['days'] 
            print('Weight of Price:',parsed_pbody['price'] )
            minrng = parsed_pbody['price'] 
            print('Weight of #Purchase:',parsed_pbody['purchase'] )
            maxrng = parsed_pbody['purchase']

        if self.path == "/":
            self.path="/index.html"
        fname = join(join(os.getcwd(),'public'),self.path[1:])
        with open(fname,"rb") as f:
            fout = f.read(os.path.getsize(fname))
            self.wfile.write(fout)

    def do_PUT(self):
        self.do_POST()

host = ''
port = 3000
HTTPServer((host, port), HandleRequests).serve_forever()
