import onionSpi
import time
import struct

def printSettings(obj):
	print "SPI Device Settings:"
	print "  bus:    %d"%(obj.bus)
	print "  device: %d"%(obj.device)
	print "  speed:    %d Hz (%d kHz)"%(obj.speed, obj.speed/1000)
	print "  delay:    %d us"%(obj.delay)
	print "  bpw:      %d"%(obj.bitsPerWord)
	print "  mode:     %d (0x%02x)"%(obj.mode, obj.modeBits)
	print "     3wire:    %d"%(obj.threewire)
	print "     lsb:      %d"%(obj.lsbfirst)
	print "     loop:     %d"%(obj.loop)
	print "     no-cs:    %d"%(obj.noCs)
	print "     cs-high:  %d"%(obj.csHigh)
	print ""
	print "GPIO Settings:"
	print "  sck:      %d"%(obj.sck)
	print "  mosi:     %d"%(obj.mosi)
	print "  miso:     %d"%(obj.miso)
	print "  cs:       %d"%(obj.cs)
	print ""

def initADC(miso, mosi, sclk, cs):
	spiDev  = onionSpi.OnionSpi(1, 32766)
	spiDev.delay = 10
	spiDev.mode = 0
	spiDev.sck = sclk
	spiDev.mosi = mosi
	spiDev.miso = miso
	spiDev.cs = cs
	spiDev.speed = 1350000 # for 3.3V supply

	spiDev.setVerbosity(0)
	# check the device
	print 'Checking if device exists...'
	ret = spiDev.checkDevice()
	print '   Device does not exist: %d'%(ret)

	# register the device
	print 'Registering the device...'
	ret = spiDev.registerDevice()
	print '   registerDevice returned: %d'%(ret)

	# initialize the device parameters
	print 'Initializing the device parameters...'
	ret = spiDev.setupDevice()
	print '   setupDevice returned: %d'%(ret)

	# check the device again
	print '\nChecking if device exists...'
	ret = spiDev.checkDevice()
	print '   Device does not exist: %d'%(ret)
	return spiDev

def poll_sensor(spiDev, channel):

    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    # first bit + single-ended with channel
    if channel == 1:
        cbyte = 0xE0
    else:
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

#main
spi = initADC(9,8,7,6)
#printSettings(spi)
:
channel = 0
adcValues = []
for i in range(100):

    monkey = poll_sensor(spi, channel)
    #volt = round (((monkey * 3300) / 1024), 0)
    print ('10 bit resolution: ' + str(monkey))
    #print ('Voltage (mV): ' + str(volt))
    #curr = round((monkey * 0.029), 0)
    #print ('Current (mA): ' + str(curr))

    time.sleep(0.0014)
