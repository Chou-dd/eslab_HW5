from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

led_light = bytes(0x00)
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            #print "Discovered device", dev.addr
            print("Discovered device", dev.addr) 
        elif isNewData:
            #print "Received new data from", dev.addr
            print ("Received new data from", dev.addr)
    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        global led_light
        print(data)
        led_light = data
        #print("handleNotification", led_light)
        
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3.0)
n=0
for dev in devices:
    #print "%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi)
    print(n, ": Device ",dev.addr, "(", dev.addrType, ")", ", RSSI= ", dev.rssi, " dB" )
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print(desc, "=", value)
number = input('Enter your device number: ')
print('Device', number)
#print(type(devices[number].addr))
print(list(devices)[int(number)].addr)
print("Connecting...")
dev = Peripheral(list(devices)[int(number)].addr, 'random')
dev.withDelegate(ScanDelegate())
print("Services...")
for svc in dev.services:
    print(str(svc))
try:
    testService = dev.getServiceByUUID(UUID(0xa000))
    for ch in testService.getCharacteristics():
        print(str(ch))
    testService = dev.getServiceByUUID(UUID(0xb000))
    for ch in testService.getCharacteristics():
        print(str(ch))
    but_ch = dev.getCharacteristics(uuid=UUID(0xa001))[0]
    cccd = but_ch.getHandle() + 1
    dev.writeCharacteristic(cccd, bytes([0x01, 0x00]))
    if (but_ch.supportsRead()):
        print(but_ch.read())
    led_ch = dev.getCharacteristics(uuid=UUID(0xb001))[0]
    if (led_ch.supportsRead()):
        print(led_ch.read())
        led_light = led_ch.read()
    while True:
        if(dev.waitForNotifications(1.0)):
            #handleNotification() was called
            #dev.writeCharacteristic(cccd, bytes([0x01]))
            #print("while", led_light)
            led_ch.write(led_light)
            continue
        print("Waiting...")
        # Perhaps do something else here
        
finally:
    dev.disconnect() 
