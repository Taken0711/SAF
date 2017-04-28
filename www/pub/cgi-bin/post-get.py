#!/usr/bin/env python
# coding: utf-8

import os
import sys

def main():
    print """<html>
    <head>
        <title>Junac - POST/GET</title>
    </head>
    <body><h3>"""
    if os.environ["QUERY_STRING"] == "":
        #i = 0
        """for line in sys.stdin.read():
            if i == 0:
                print "POST de POST/GET "
            print line
            i += 1
        if i != 0:
            print "Pas de chaine ni dans le GET ni dans le POST" """
        body = sys.stdin.read()
        if body != "":
            print "POST de POST/GET " + body
        else:
            print "Pas de chaine ni dans le GET ni dans le POST"

    else:
        print "GET de POST/GET " + os.environ["QUERY_STRING"]
    print """</h3></body>
    </html>"""


main()
