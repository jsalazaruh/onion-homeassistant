#!/usr/bin/env python

import time
import onionGpio
import paho.mqtt.publish as publish
from datetime import datetime

#LED and PIR GPIO
led_pin = 1
pir_pin = 2
led_light_up_time = 5

broker = "IP_ADDRESS"

topic = "YOUR_TOPIC_HERE"

#Assigning pins to onion
led = onionGpio.OnionGpio(led_pin)
pir = onionGpio.OnionGpio(pir_pin)

#Setting direction of pins 
led.setOutputDirection(0)
pir.setInputDirection()

#Start of loop for motion detection
while True:
    value = pir.getValue().rstrip()
    if(value == "1"):
        print datetime.now(),
        print "motion_detected"
        #If detected, it will try to send string package to the broker
        try:
            publish.single(topic, "OCCUPIED", hostname=broker, port=1883)
        except:
            pass
        #Turning on led if PIR is high
        led.setValue(1)
        time.sleep(led_light_up_time)
    else:
        #If nothing is detected, it will leave led low  
        led.setValue(0)
        print datetime.now(),
        print "no_motion"
        try:
            #It will notify the user that nothing is being detected
            publish.single(topic, "AWAY", hostname=broker, port=1883)
        except:
            pass
        time.sleep(3)
