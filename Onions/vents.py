#This code's mainly use is for a single onion omega with multiple servo motors by using the PWM expansion dock 
#All of the smart vents are being controlled by one topic
#The vents can be changed by the package that the broker is sending to the client

import paho.mqtt.client as mqtt
import subprocess
import time

broker="YOUR_IP_HERE"

#The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    #Subscribing in on_connect() means that if we lose the connection and
    #reconnect then subscriptions will be renewed.
    client.subscribe("home/vents")

#The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if "V1_OPEN" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '0', '9'])
        print "V1_OPEN"
    
    elif "V1_CLOSE" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '0', '1'])
        print "V1_CLOSE"
    
    elif "V1_HALF" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '0', '6'])
        print "V1_HALF"
		
    elif "V2_OPEN" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '1', '9'])
        print "V2_OPEN"
    
    elif "V2_CLOSE" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '1', '1'])
        print "V2_CLOSE"
	  
    elif "V2_HALF" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '1', '6'])
        print "V2_HALF"	
		
    elif "V3_OPEN" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '2', '9'])
        print "V3_OPEN"
    
    elif "V3_CLOSE" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '2', '1'])
        print "V3_CLOSE"
	  
    elif "V3_HALF" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '2', '6'])
        print "V3_HALF"
				
    elif "V4_OPEN" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '3', '9'])
        print "V4_OPEN"
    
    elif "V4_CLOSE" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '3', '1'])
        print "V4_CLOSE"
	  
    elif "V4_HALF" in msg.payload:
        subprocess.call(['pwm-exp', '-i', '3', '6'])
        print "V4_HALF"		
		
    else:
        print "Invalid"

    print(msg.topic+" "+str(msg.payload))
	

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
	client.connect(broker, 1883, 60)
except:
	pass
	
client.loop_forever()
