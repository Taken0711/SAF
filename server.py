#!/usr/bin/env python
# coding: utf-8

import socket
import os
import subprocess


PROPERTIES = {}
ERRORS = {"400": "Bad Request", "404": "Not Found", "405": "Method Not Allowed"}

class MethodNotAllowed(Exception):
    def __init__(self, message):
        self.message = message

def get(first_line):
    path = first_line.split(" ")[1].strip()
    print "[INFO ] Requested file: " + path
    if path == "/":
        path = "/index.html"
    if path.startswith("/"+PROPERTIES["CGI-BIN_DIRECTORY"]+"/"):
        if path.startswith(
                "/"+PROPERTIES["CGI-BIN_DIRECTORY"]+"/"+PROPERTIES["POST_ONLY_DIRECTORY"]):
            raise MethodNotAllowed("GET method isn't allowed on requested file")
        os.environ["QUERY_STRING"] = path.split("?")[1]
        pls = subprocess.Popen(
            [PROPERTIES["HTTP_ROOT"] + path.split("?")[0]], stdout=subprocess.PIPE)
        return pls.stdout.read()
    else:
        with open(PROPERTIES["HTTP_ROOT"] + path) as f:
            return f.read()

def post(first_line, body):
    path = first_line.split(" ")[1].strip()
    print "[INFO ] Requested file: " + path
    if path.startswith("/"+PROPERTIES["CGI-BIN_DIRECTORY"]+"/"):
        if path.startswith(
                "/"+PROPERTIES["CGI-BIN_DIRECTORY"]+"/"+PROPERTIES["GET_ONLY_DIRECTORY"]):
            raise MethodNotAllowed("POST method isn't allowed on requested file")
        print PROPERTIES["HTTP_ROOT"] + path
        pls = subprocess.Popen(
            [PROPERTIES["HTTP_ROOT"] + path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        pls.stdin.write(body)
        pls.stdin.close()
        return pls.stdout.read()

def send_ok(client, body):
    answer = "HTTP/1.1 200 OK"
    res = answer+"\n\n"+body
    print "[INFO ] Send: " + answer
    client.sendall(res)

def send_error(client, code, msg):
    error = str(code) + " " + ERRORS[str(code)]
    answer = "HTTP/1.1 " + error
    body = """<html>
    <head>
        <title>"""+error+"""</title>
    </head>
    <body>
    <h1>Error """+error+"""</h1>
    <h3>"""+msg+"""</h3></body>
    </html>
    """
    res = answer+"\n\n"+body
    print "[ERROR] " + error
    client.sendall(res)

def client_read(client):
    return client.recv(int(PROPERTIES["BUFFER_SIZE"]))


def load_properties():
    try:
        with open("server.properties") as f:
            for line in f:
                tmp = line.strip().replace(" ", "").split("=")
                PROPERTIES[tmp[0]] = tmp[1]
        print "[INFO ] Detected properties: " + str(PROPERTIES)
    except IOError:
        print "[FATAL] Cannot open server.properties. Make sure that the properties file is in the same directory as the server"
        exit(0)


def main():
    print "[INFO ] Starting server..."
    load_properties()
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sckt.bind((PROPERTIES["ADRESS"], int(PROPERTIES["PORT"])))
    print "[INFO ] Now listening on " + PROPERTIES["ADRESS"] + ":" + str(PROPERTIES["PORT"]) +"\n"

    while True:
        sckt.listen(5)
        client, address = sckt.accept()
        print "[INFO ] {} connected".format(address)
        os.environ["QUERY_STRING"] = ""

        # --- Reading the request

        try:
            request = client_read(client)
            if request == "":
                continue

            # Extract the first line
            while "\n" not in request:
                request += client_read(client)
            tmp = request.split("\n")
            first_line = tmp[0].strip()
            method = first_line.split(" ")[0]
            print "[INFO ] Request: "+first_line
            request = "\n".join(tmp[1:])

            # Extract headers
            while "\n\n" not in request.replace("\r", ""):
                request += client_read(client)
            headers = {}
            tmp = request.split("\n")
            i = 0
            for line in tmp:
                striped_line = line.strip()
                if striped_line == "":
                    break
                headers[striped_line.split(":")[0].lower()] = striped_line.split(":")[1]
                i += 1
            request = "\n".join(tmp[i+1:])
            print "[INFO ] Headers: " + str(headers)

            # Choose the right method and send answer
            if method == "GET":
                send_ok(client, get(first_line))
            elif method == "POST":
                size = int(headers["content-length"])
                body = request
                while len(body) < size:
                    line = client_read(client)
                    body += line
                print "[INFO ] Body:" + body
                send_ok(client, post(first_line, body))
            else:
                raise Exception()
        except (IOError, OSError):
            send_error(client, 404, "The requested file was not found on this server")
        except MethodNotAllowed as e:
            send_error(client, 405, e.message)
        except Exception as e:
            send_error(client, 400, "The request wasn't undertood by the server")
        client.close()
        print "[INFO ] {} disconnected\n".format(address)

        # --- End of reading

    print "[INFO ] Closing server..."
    client.close()
    sckt.close()
    print "[INFO ] Server is now closed properly"

main()
