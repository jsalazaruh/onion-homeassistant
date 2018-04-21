#!/usr/local/bin/python

import time
import onionGpio
import paho.mqtt.publish as publish
from datetime import datetime

# LED GPIO
led_pin = 1
pir_pin = 2
led_light_up_time = 5

broker = "IP_ADDRESS"

topic = "room/presence1"

led = onionGpio.OnionGpio(led_pin)
pir = onionGpio.OnionGpio(pir_pin)

led.setOutputDirection(0)
pir.setInputDirection()

while True:
   value = pir.getValue().rstrip()
   if(value == "1"):
         print datetime.now(),
         print "motion_detected"
         try:
             publish.single(topic, "OCCUPIED", hostname=broker, port=1883)
         except:
             pass
         led.setValue(1)
         time.sleep(led_light_up_time)
   else:
         led.setValue(0)
         print datetime.now(),
         print "no_motion"
         try:
             publish.single(topic, "AWAY", hostname=broker, port=1883)
         except:
             pass
         time.sleep(1)
