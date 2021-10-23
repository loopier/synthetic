#!/usr/bin/env python

# Supercollider code:
# ------------------
# // boot network connection
# n = NetAddr("127.0.0.1", 1234);
# // set reply address
# n.sendMsg("/replyTo", n.ip, 57120);
# // function-name, path-to-csv, num-of-fields, percent-of-original, tag
# n.sendMsg("/oversampling", "tuned_before_the_rain.dat", 6, 1, "'the'");

import argparse

import random

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

import synthetic as syn

serverport = 1234
serverIp = "127.0,0,1"

client = None

def setDestination(*args):
    "Return IP address of the MSG sender."
    ip = list(args)[-2]
    port = list(args)[-1]
    print(ip, port)
    global client
    client =  udp_client.SimpleUDPClient(ip, port)

def synthetic(func, path_to_data, d, ratio, tag):
    print(path_to_data, d, ratio)
    data = syn.syntheticOversampling(path_to_data,d,ratio)
    tagged = getTagFromData(tag, data)
    index = random.randrange(len(tagged))
    choice = tagged[index]
    print("tagged: ", len(tagged))
    print("rand: ", index)
    print("choice: ", choice)
    global client
    client.send_message("/synthetic", choice)

def getTagFromData(tag, data):
    tagged = []
    for x in data:
        if x[-1] == tag:
            print(tag + ": " + str(x))
            tagged.append(x)
    print("\n")
    return tagged

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="Listen IP")
    parser.add_argument("--port", default=1234, help="Listen port")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/*", print)
    dispatcher.map("/oversampling", synthetic)
    dispatcher.map("/replyTo", setDestination)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("OSC listening on {}".format(server.server_address))
    server.serve_forever()
