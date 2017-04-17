#!/usr/bin/env python
#
# $Id: menu_switch_class.py,v 1.3 2016/10/16 09:24:12 bob Exp $
# Raspberry Retro Pi Internet Radio
# Retro radio menu switch
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#

import RPi.GPIO as GPIO
import time


# Status LED class
class MenuSwitch:
	# Status settings
	CLEAR = 0
	VALUE1 = 1
	VALUE2 = 2
	VALUE4  = 4 
	switch1 = None
	switch2 = None
	switch4 = None

	def __init__(self, switch1, switch2, switch4,callback):
		self.switch1 = switch1
		self.switch2 = switch2
		self.switch4 = switch4
		self.callback = callback

		# Set up switch lines
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		if self.switch1 > 0:
			GPIO.setup(self.switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		if self.switch2 > 0:
			GPIO.setup(self.switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		if self.switch4 > 0:
			GPIO.setup(self.switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Add event detection to the GPIO inputs
		if self.switch1 > 0:
			GPIO.add_event_detect(self.switch1, GPIO.BOTH, callback=self.callback, bouncetime=100)
		if self.switch2 > 0:
			GPIO.add_event_detect(self.switch2, GPIO.BOTH, callback=self.callback, bouncetime=100)
		if self.switch4 > 0:
			GPIO.add_event_detect(self.switch4, GPIO.BOTH, callback=self.callback, bouncetime=100)
                return

	# Get switch state
	def get(self):
		value = 0
		if not GPIO.input(self.switch1): 
			value  += 1
		if not GPIO.input(self.switch2): 
			value  += 2
		if not GPIO.input(self.switch4): 
			value  += 4
		return value


if __name__ == "__main__":

	switch_value = 0 

	def menu_switch_event(switch):
		global switch_value
		time.sleep(0.1)
		value = menu_switch.get()
		if value != switch_value:
			print "Switch", switch,"Value =", value
			switch_value = value
		return

	menu_switch = MenuSwitch(24,8,7,menu_switch_event)
	switch_value = menu_switch.get()

	while True:
		time.sleep(0.1)

# End of class
