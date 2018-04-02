# onion-homeassistant
Creating IoT devices with Onion Omega 2 plus, MQTT and Homeassistant. 

# Introduction: 

The purpose of this project is to create IoT devies with the use of the Onion Omega 2+ and Homeassistant. Communication between the clients and Homeassistant are done using MQTT protocol. Python is the primary language used in order to create these devices. 

Setting up Homeassistant for Onion Omega:

In order to fully intergrate the Onion Omega 2+ with Homeassistant, you must first edit the Homeassistant ```configuration.yaml```: 

## Local MQTT broker: 

All devices will be set up to work locally. The Onion Omega's will need to have the Eclipse-paho mqtt client installed to serve as a client to the homeassistant broker. [Link to the Eclipse paho mqtt client page](https://www.eclipse.org/paho/clients/python/docs/)

```
mqtt:
  broker: 127.0.0.1
  port: 1883
```

## LED switch:

To fully understand how the IoT device works, we must first create a simple switch. This configuration will be able to send and receive a binary state to the device. The messages sent/received are 'message payloads.' When the client(Onion Omega 2+) receives the 'ON' message, it will trigger the GPIO pin to become high. Likewise, when the client receives the message 'OFF', it will set the pin to low.

Given that the client only receives commands from the broker, we only need a ```command_topic```.

```
light: 
  - platform: mqtt
  - command_topic: "light/dev"
  - payload_on: "ON"
  - payload_off: "OFF"
```

## Digital Humidity/Temperature Sensor (DHT11)

By using OPKG (package manager), you are able to install the DHT11/DHT22 package to use the sensors. [Link to the Onion page to set up sensors.](https://onion.io/2bt-reading-dht-sensor-data/) Highly recommend you set up sensors and learn how they work before continuing. 

```state_topic``` is being used to updated the broker on the state of the client. 

```
  - platform: mqtt
    state_topic: "home/sensor"
    name: "Temp"
    unit_of_measuremnt: "Fahrenheit"
    value_template: "{{value_json.temperature}}"
  
  - platform: mqtt
    state_topic: "home/sensor"
    name: "Humidity"
    unit_of_measurement: "%"
    value_template: "{{value_json.humidity}}"
```
    
## Motion Detection (Passive Infrared Sensor)

Similarly, this works the same as the Temperature/humidity client. A ```state_topic``` is needed. 

```
  - platform: mqtt
    state_topic: "home/motion"
    name: "Motion Dev"
    qos: 0
    payload_on: "ON"
    payload_off: "OFF"
```
## Power Monitoring (Currently working on)

Becasue I did not want to use an arduino Expansion Dock, I decided to implement an ADC to receive analog data and convert it to digital in order to have more control on the data. Communication with the ADC is done through the Serial Peripheral Interface bus. [ADC MCP3008](https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf) I am using a [non-invasive current sensor](https://www.sparkfun.com/products/11005) to read AC current from the appliances. 

Update: I will upload the voltage divider diagram along with the burder resistor used to obtain an accurate readings. 
