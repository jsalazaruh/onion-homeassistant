import subprocess
import time
import paho.mqtt.publish as publish
import json

#Start loop for digital humidity temperature sensor  
while True:
    humidity1 = 0
    temperature1 = 0
    #Using opkg package to read the dht sensor with onion and then saving the output in JSON format to 'process'
    process = subprocess.Popen(['dht-sensor', '0', 'DHT11', 'json'],stdout=subprocess.PIPE)

    stdout = json.loads(process.communicate()[0])

    #Creating tuples for organization
    humidity1 = stdout["humidity"]
    temperature1 = stdout["temperature"]
    print(humidity1, temperature1)
    #Comparing data in order to verify authenticity of data
    if(temperature1 < -200 and humidity1 < -200):
        print("Problem")
    else:
        str = json.dumps(stdout)
        try:
            #Trying to send json package to topic, if it doesn't reach a connection 
            #it will pass the loop without returning any errors
            publish.single("YOUR_TOPIC_HERE", str, hostname="YOUR_IP_HERE", port=1
        except:
            pass
    time.sleep(3)
