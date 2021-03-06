# coding: utf-8
import SocketServer
import httphandler
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright (C) 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

SITE_ROOT = "www"

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # ACTIONS: Make request, Process Response, Send Response
        http_request = httphandler.HTTPRequest(self.data, SITE_ROOT)
        site_content_path = os.path.realpath(SITE_ROOT)
        http_response = httphandler.HTTPResponse(site_content_path, http_request) 
        self.request.sendall(http_response.MakeResponse())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    try:
        SocketServer.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080
        server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
        print("Starting HTTP Server on PORT: %s\r\n" % PORT)

        # Activate the server; this will keep running forever
        server.serve_forever()

    except KeyboardInterrupt:
        # Interrupt the program with Ctrl-C and close server.
        print("\r\nClosing Server with ^C\r\n")
        server.socket.close()
