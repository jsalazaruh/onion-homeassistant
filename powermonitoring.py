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
def initADC(miso, mosi, sclk, cs):
    spiDev  = onionSpi.OnionSpi(1, 32766)
    spiDev.delay = 10
    spiDev.mode = 0
    spiDev.sck = sclk
    spiDev.mosi = mosi
    spiDev.miso = miso
    spiDev.cs = cs
    spiDev.speed = 1350000 

    spiDev.setVerbosity(0)
    print 'Checking if device exists...'
    out = spiDev.checkDevice()
    print '   Device does not exist: %d'%(out)

    print 'Registering the device...'
    out = spiDev.registerDevice()
    print '   registerDevice returned: %d'%(out)

    print 'Initializing the device parameters...'
    out = spiDev.setupDevice()
    print '   setupDevice returned: %d'%(out)

    print '\nChecking if device exists...'
    out = spiDev.checkDevice()
    print '   Device does not exist: %d'%(out)

    return spiDev

#function to obtain data 
def poll_sensor(spiDev, channel):

    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    #leading bit + 
    if channel == 1:
	#11100000
        cbyte = 0xE0
    else:
	#11000000
        cbyte = 0xC0

    #first bit and single with channel, readByte is already MSBF
    spiResp = spiDev.readBytes(cbyte, 3)

    byte0 = spiResp[0]
    byte1 = spiResp[1]
    byte2 = spiResp[2]

    #print channel
    #print cbyte
    print (byte0, byte1, byte2)

    return 0x3FF & ((byte0 & 0x01) << 9 | (byte1 & 0xFF) << 1 | (byte2 & 0x80) >> 7 )

#start of main program 
spi = initADC(9,8,7,6)

channel = 0
adcValues = []
for i in range(100):

    monkey = poll_sensor(spi, channel)
    #volt = round (((monkey * 3300) / 1024), 0)
    print ('10 bit resolution: ' + str(monkey))
    #print ('Voltage (mV): ' + str(volt))
    
    #Sampling rate at 60Hz for hairdryer, becasue of Nyquist Theorem, we want to get 10 times the amount of samples
    #to obtain an accurate reading. Anything above samplerate * 2 will be fine  
    time.sleep(0.0014)
