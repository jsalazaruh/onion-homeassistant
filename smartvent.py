#!/usr/bin/env python

import paho.mqtt.client as mqtt
import subprocess
import time

broker="1your_ip_here"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("home/vents")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if "OPEN" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '8', '9'])
        print "OPEN"
    elif "CLOSE" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '8', '1'])
        
        print "CLOSE"
    else:
        subprocess.call(['pwm-exp', '-i', '8', '6'])
        #process = subprocess.Popen(['pwm-exp', '-i', PWM_pin, '9'],
        #stdout=subprocess.PIPE)
        #stdout = process.communicate()[0]
        print "HALF"


    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# broker configuration
client.connect(broker, 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
