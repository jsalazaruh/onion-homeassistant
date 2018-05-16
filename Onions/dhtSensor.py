import subprocess
import time
import paho.mqtt.publish as publish
import json

while True:
    humidity1 = 0
    temperature1 = 0
    process = subprocess.Popen(['dht-sensor', '0', 'DHT11', 'json'],
    stdout=subprocess.PIPE)

    stdout = json.loads(process.communicate()[0])

    #creating tuples for organization
    humidity1 = stdout["humidity"]
    temperature1 = stdout["temperature"]
    print(humidity1, temperature1)
#comparing data in order to verify authenticity of data
    if(temperature1 < -200 and humidity1 < -200):
        print("Problem")
    else:
        str = json.dumps(stdout)
        try:
            publish.single("YOUR_TOPIC_HERE", str, hostname="YOUR_IP_HERE", port=1
        except:
            pass
    time.sleep(3)
