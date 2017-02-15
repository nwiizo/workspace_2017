#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

def get_py():
        target_host = "153.121.43.113"
        target_port = 80

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host,target_port))
        client.send("GET / \r/ Host/1.1\r\n\r\n")
        response = client.recv(8096)
        print (response)

get_py()

