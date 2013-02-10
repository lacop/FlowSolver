from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from sys import argv
from time import sleep

path = argv[1]
lines = open(path).readlines()

device = MonkeyRunner.waitForConnection()

DURATION = 0.01
STEPS = 1

down = False
lx, ly = 0, 0
for l in lines:
	x, y = l.split(' ')
	x = int(x)
	y = int(y)
	
	if x == 0 and y == 0:
		# End gesture
		print 'up'
		#device.touch(lx, ly, MonkeyDevice.UP)
		down = False
	else:
		if down:
			device.drag((lx, ly), (x, y), DURATION, STEPS)
		else:
			down = True
	lx = x
	ly = y
	#sleep(0.1)
			
print 'Done'
