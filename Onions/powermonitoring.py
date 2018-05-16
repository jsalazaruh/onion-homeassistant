#!/usr/bin/env python

import time
import onionSpi
import json
import paho.mqtt.publish as publish
from decimal import Decimal

#Assigning the pins for spi bus and assigning the clock speed for 3.3V
def ADC(miso, mosi, sclk, cs):
    spiDev  = onionSpi.OnionSpi(1, 32766)
    spiDev.delay = 10
    spiDev.mode = 0
    spiDev.sck = sclk
    spiDev.mosi = mosi
    spiDev.miso = miso
    spiDev.cs = cs
    spiDev.speed = 1200000

    spiDev.setVerbosity(0)

    return spiDev

#function to obtain data
def polling_sensor(spiDev, channel):

    #only used when inputed, may change in the future
    #assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    #leading bit + single-ended mode or pseudo-differential + channel. The rest
    #look at http://www.farnell.com/datasheets/1599363.pdf for more information
    #channel 0 is set as default
    if channel == 0:
        #1101 0000
        hexbyte = 0xD0

    #the function is going to send 3 bytes to the TX and RX buffer would be too
    #you need to do use the function this way to work or it will return all ones
    #https://github.com/OnionIoT/spi-gpio-driver/blob/master/src/python/python-o
    resp = spiDev.readBytes(hexbyte, 2)

    byte0 = resp[0]
    byte1 = resp[1]

	#converting the 2 bytes of data into 10 bits with bitwise operators
    return 0x3FF & ((byte0 << 7) | (byte1 >> 1))


#main
while True:
    spi = ADC(9,8,7,6)
    num_of_samples = 600
    ical = 60.6
    sumI = 0
    channel = 0
    sampleI = 512
    filteredI = 0

    #sampling at 600 becasue I want avoid any aliasing problems 
    #it also deletes the offset of 512 resolution from the voltage divider and 
    #implements a digital low pass filter to correct the phase shift 
    for i in range(num_of_samples):
        last_sampleI = sampleI
        sampleI = polling_sensor(spi, channel)
        last_filteredI = filteredI
        filteredI = 0.996 * (last_filteredI + sampleI - last_sampleI)
        sqI = filteredI * filteredI
        sumI += sqI


    i_ratio = ical * ((3300 / 600) / 1023)
    irms = i_ratio * (sumI / num_of_samples)**(0.5)
    #Since we are using a hairdryer for prototyping, I need to figure out how much Vrms is using
    #after research I later found that it uses a total of 125 Vrms
    power = 125 * irms
    #rouding down & converting into a string for the MQTT broker 
    y = round(power,3)
    x = str(y)

    print(x)
	try: 
	    #trying to send data to broker 
        publish.single("YOUR_TOPIC_HERE", x, hostname="IP_GOES_HERE", port=1883)
	except:
	    pass
	time.sleep(3)
