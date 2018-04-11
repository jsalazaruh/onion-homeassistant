#!/usr/bin/env python

import time
import onionSpi
import struct

#printing settings for spi bus
def printSettings(obj):
    print "SPI Device Settings:"
    print "  bus:      %d"%(obj.bus)
    print "  device:   %d"%(obj.device)
    print "  speed:    %d Hz (%d kHz)"%(obj.speed, obj.speed/1000)
    print "  delay:    %d us"%(obj.delay)
    print "  bpw:      %d"%(obj.bitsPerWord)
    print "  mode:     %d (0x%02x)"%(obj.mode, obj.modeBits)
    print "  3wire:    %d"%(obj.threewire)
    print "  lsb:      %d"%(obj.lsbfirst)
    print "  loop:     %d"%(obj.loop)
    print "  no-cs:    %d"%(obj.noCs)
    print "  cs-high:  %d"%(obj.csHigh)
    print " "
    print "GPIO Settings:"
    print "  sck:    %d"%(obj.sck)
    print "  mosi:   %d"%(obj.mosi)
    print "  miso:   %d"%(obj.miso)
    print "  cs:     %d"%(obj.cs)
    print " "

#assigning the pins for spi bus and assigning the clock speed for 3.3V
def ADC(miso, mosi, sclk, cs):
    spiDev  = onionSpi.OnionSpi(1, 32766)
    spiDev.delay = 10
    spiDev.mode = 0
    spiDev.sck = sclk
    spiDev.mosi = mosi
    spiDev.miso = miso
    spiDev.cs = cs
    spiDev.speed = 1350000 
    
    #chekcing if device is in existance
    spiDev.setVerbosity(0)
    print 'Checking if device exists...'
    out = spiDev.checkDevice()
    print '   Device does not exist: %d'%(out)

    #Registering device with spiDev
    print 'Registering the device...'
    out = spiDev.registerDevice()
    print '   registerDevice returned: %d'%(out)
    
    #chekcing to see for parameters
    print 'Initializing the device parameters...'
    out = spiDev.setupDevice()
    print '   setupDevice returned: %d'%(out)

    return spiDev

#function to obtain data 
def polling_sensor(spiDev, channel):

    #only used when inputed, may change in the future
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    #leading bit + single-ended mode or pseudo-differential + channel. The rest of the 8 bit configuration is filled with zeros
    #look at http://www.farnell.com/datasheets/1599363.pdf for more information about spi bus configuration. Page 15 of 34
    #channel 0 is set as default
    if channel == 1:
	#11100000
        hexbyte = 0xE0
    #11000000
    	hexbyte = 0xC0

    #the function is going to send 3 bytes to the TX and RX buffer would be too large to read
    #you need to do use the function this way to work or it will return all ones
    #https://github.com/OnionIoT/spi-gpio-driver/blob/master/src/python/python-onion-spi.c#L131
    resp = spiDev.readBytes(hexbyte, 3)

    byte0 = resp[0]
    byte1 = resp[1]
    byte2 = resp[2]

    #print channel
    #print cbyte
    #print (byte0, byte1, byte2)
	
    #the response of the adc will be spread throughout 3 bytes so we need to shift to the bits
    #to the left and will be 10 bits (hence why it's a 10 bit ADC) 
    return 0x3FF & ((byte0 & 0x01) << 9 | (byte1 & 0xFF) << 1 | (byte2 & 0x80) >> 7 )

#start of main 
spi = ADC(9,8,7,6)
'''
channel = 0
adcValues = []
for i in range(20):

    monkey = polling_sensor(spi, channel)
    #volt = round (((monkey * 3300) / 1024), 0)
    print ('10 bit resolution: ' + str(monkey))
    #print ('Voltage (mV): ' + str(volt))
    
    #Sampling rate at 60Hz for hairdryer, becasue of Nyquist Theorem, we want to get 10 times the amount of samples
    #to obtain an accurate reading. Anything above samplerate * 2 will be fine  
    time.sleep(0.0014)
'''

sumtot = 0
channel = 0
#on EmonLib, this is (ADC_COUNT >> 1), which will equal 5
#ADC_COUNT is 10 because it is using the 10 bit configuration
offsetI = 5
adcValues = []
for i in range(1000):

    monkey = poll_sensor(spi, channel)

    offsetI = (offsetI + (monkey - offsetI)/1024)
    filtered = monkey - offsetI

    sqI = filtered * filtered

    sumtot += sqI

iratio = 27.78 * (3.3/10)

irms = iratio * (sumtot/1000)**2

print("{} is the rms for the current".format(irms))
    #time.sleep(0)
