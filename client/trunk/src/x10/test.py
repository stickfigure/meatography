import serial

#tty = "/dev/tty.usbserial"
tty = "/dev/ttyUSB0"
#tty = "/dev/ttyS1"

start = 0x02
send = 0x63
house = 0x40
unit = 0x4c
cmd = 0x45
repeat = 0x41

def main():
	port = serial.Serial(tty, 9600, timeout=1)
	port.open()
	result = port.read()
	print "Initial crap: '" + result + "', length=" + str(len(result)) 
	
	port.write(chr(0x02))
	result = port.read()
	print "After write: '" + result + "', length=" + str(len(result))
	print "Firstchar is '" + hex(ord(result[0])) + "'"
	
	port.close()
	
main()