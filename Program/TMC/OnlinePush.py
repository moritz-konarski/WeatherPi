from __future__ import print_function
import paho.mqtt.publish as publish
import string
import random

string.alphanum='1234567890avcdefghijklmnopqrstuvwxyzxABCDEFGHIJKLMNOPQRSTUVWXYZ'

channelID = "670883"

writeAPIKey = "XS5NVT4DW89EVFQ8"

mqttHost = "mqtt.thingspeak.com"

mqttUsername = "Weather_Pi"

mqttAPIKey =" 	F2F7UZCT9442AXK2"

tTransport = "websockets"
tPort = 80

topic = "channels/" + channelID + "/publish/" + writeAPIKey

class OnlinePush:

    def __init__(self):
        pass

    def push(self, dht_values=[[]], out_temp=[], light=[]):
        clientID = ''

        for x in range(1,16):
            clientID+=random.choice(string.alphanum)

        payload = "field1={}&field2={}&field3={}&field4={}".format(dht_values[0][0], dht_values[0][1], out_temp[0], light[0])
        

        try:
            publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort, auth={'username':mqttUsername,'password':mqttAPIKey})
            print("pushing")

        except:
            print("There was an error while publishing the data.")