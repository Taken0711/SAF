#!/usr/bin/env python
# coding: utf-8

import os
import sys

def main():
    print "Content-type: text/html\n"
    print """<html>
    <head>
        <title>Junac - POST/GET</title>
    </head>
    <body><h3>"""
    try:
        if os.environ["QUERY_STRING"] != "":
            print "GET de POST/GET " + os.environ["QUERY_STRING"]
        else:
            raise KeyError
    except KeyError:
        body = sys.stdin.read()
        if body != "":
            print "POST de POST/GET " + body
        else:
            print "Pas de chaine ni dans le GET ni dans le POST"

    print """</h3></body>
    </html>"""


main()
