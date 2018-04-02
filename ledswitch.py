#!/usr/bin/python3

import onionGpio
import paho.mqtt.client as mqtt

#intializing GPIO & topic

command_topic = "office/light/switch"

gpio0 = onionGpio.OnionGpio(0)
gpio0.setOutputDirection(0)

#confirming connection with MQTT broker
def on_connect(client, data, flags, rc):
    
	client.subscribe(command_topic)
	
	print('Connected, rc: ' + str(rc))
	
#reading/processing data from the broker
def on_message(client, userdata, msg):
	
	if "ON" in msg.payload:
		gpio0.setValue(1)
	elif "OFF" in msg.payload:
	    gpio0.setValue(0)
	else:
	    gpio0.setValue(0)
	
	print("Topic: "+ msg.topic+"\nMessage: "+str(msg.payload))
#
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()