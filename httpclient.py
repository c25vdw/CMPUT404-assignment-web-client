#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
from typing import List
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __repr__(self):
        return f"{self.code} body: <{self.body}>"

class HTTPClient(object):
    DEFAULT_PORT = 80 
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, headers):
        for header in headers:
            if header.startswith('HTTP'):
                return int(header.split(' ')[1])
        return None

    def get_headers_body(self,data):
        [headers, body] = data.split('\r\n\r\n')
        headers = headers.split('\r\n')
        return headers, body

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
            print(part)
        return buffer.decode('utf-8')

    def prepare_host(self, url):
        return url.split('://')[1].split('/')[0]

    def prepare_path(self, url):
        without_protocol = url.split('://')[1]
        path_start = without_protocol.find('/')
        if path_start == -1:
            return '/'
        return without_protocol[path_start:]

    def prepare_port(self, url):
        if len(url.split('://')[1].split(':')) > 1:
            return int(url.split('://')[1].split(':')[1].split('/')[0])
        return 80

    def GET(self, url, args=None):
        try:
            host = self.prepare_host(url)
            port = self.prepare_port(url)

            # prepare header
            buf = f"""GET {self.prepare_path(url)} HTTP/1.1\r
Host: {self.prepare_host(url)}\r
User-Agent: Python/3.6\r
Accept: */*\r
\r\n""" 
            print(buf, host, port)
            # connect
            self.connect(self.prepare_host(url).split(':')[0], self.prepare_port(url))
            # send request
            self.sendall(buf)

            data = self.recvall(self.socket)
            #
            headers, body = self.get_headers_body(data)
            code = self.get_code(headers)
            print(f"response code {code}, body: {body}")
            self.socket.close()
            return HTTPResponse(code, body)
        finally:
            pass

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
