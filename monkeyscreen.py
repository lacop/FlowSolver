from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from sys import argv

path = 'screenshots/default.png'
if len(argv) > 1:
	path = argv[1]

device = MonkeyRunner.waitForConnection()
img = device.takeSnapshot()
img.writeToFile(path, 'png')

