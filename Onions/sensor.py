import subprocess
import time
import paho.mqtt.publish as publish

broker="ADDRESS"

topic = "home/sensor4"

while True:

    process = subprocess.Popen(['dht-sensor', '0', 'DHT11', 'json'],
    stdout=subprocess.PIPE)

    stdout = process.communicate()[0]
    print stdout

    publish.single(topic, stdout, hostname=broker, port=1883)
    time.sleep(10)
