#!/usr/bin/env python

import subprocess
import json
import time
import paho.mqtt.publish as publish

#loads temp & humidity with sensor and saves in JSON format, make sure you change the pin number
first = json.loads(subprocess.check_output('dht-sensor 3 DHT11 json',shell=True))
time.sleep(6)
second = json.loads(subprocess.check_output('dht-sensor 3 DHT11 json',shell=True))

#creating tuples for organization
humidity1 = first['humidity']
print(humidity1, humidity2)
humidity2 = second['humidity']
temperature1 = first['temperature']
print(temperature1, temperature2)
temperature2 = second['temperature']

#comparing data in order to verify authenticity of data
if(abs(humidity1 - humidity2) > 2 or abs(temperature1 - temperature2) > 2 or temperature1 < -200 or temperature2 < -200 or humidity1 < -200 or humidity2 < -200):
    print("Problem")
else:
    str = json.dumps(second)
    print(str)
    try:
        publish.single("home/sensor", str, hostname="10.0.0.174", port=1883)
    except:
        pass
time.sleep(6)
