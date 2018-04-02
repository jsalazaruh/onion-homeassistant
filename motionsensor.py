import time
import onionGpio
import paho.mqtt.publish as publish

gpio1 = onionGpio.OnionGpio(1)

gpio1.setInputDirection()

while True:
    value = gpio1.getValue().rstrip()

    if (value == "1"):
        print "Motion Detected"
        publish.single("sensor/motion1", "ON", hostname="10.0.0.174", port=1883)
        time.sleep(5)
        publish.single("sensor/motion1", "OFF", hostname="10.0.0.174", port=1883

    time.sleep(0.1)

~
