#!/usr/bin/env python

import time
import onionGpio
import paho.mqtt.publish as publish

#initializing gpio and setting direction
gpio1 = onionGpio.OnionGpio(1)
gpio1.setInputDirection()

#start of loop to detect motion
while True:

    #conerting to string for boolean comparison
    value = str(gpio1.getValue())

    if (value == "1"):
        print "Motion Detected"
        publish.single("enter_topic_here", "ON", hostname="enter_ip", port=1883)
        time.sleep(5)
        publish.single("enter_topic_here", "OFF", hostname="enter_ip", port=1883)

    time.sleep(0.1)
