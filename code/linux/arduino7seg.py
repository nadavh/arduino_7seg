#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import commands
import traceback

class ArduinoDisplayLCD:
	def __init__ (self, device="/dev/ttyUSB0", speed=9600):
		# constants
		self.device = device;
		self.speed  = speed;

		self.digit_dict		= {}
		self.digit_dict[" "]	= "00"
		self.digit_dict["0"]	= "af"
		self.digit_dict["1"]	= "06"
		self.digit_dict["2"]	= "6b"
		self.digit_dict["3"]	= "4f"
		self.digit_dict["4"]	= "c6"
		self.digit_dict["5"]	= "cd"
		self.digit_dict["6"]	= "ed"
		self.digit_dict["7"]	= "07"
		self.digit_dict["8"]	= "ef"
		self.digit_dict["9"]	= "cf"
		self.digit_dict["-"]	= "40"

		# variables
		self.digits			= ["00", "00", "00", "00"]
		self.extra_leds		= [False, False, False, False]

		# objects
		try:
		  self.dev = serial.Serial(device, speed)
		except:
		  print "Error: can't open serial device: %s" % device
		  #traceback.print_exc()
		  exit(1)

	def close(self):
		self.dev.close()

	def updateDisplay(self):
		data_string = ""
		for i in xrange(len(self.digits)):
			if (self.extra_leds[i] == True):
				data_string = data_string + "%02x" % (int("0x" + self.digits[i],16) | 0x10)
			else:
				data_string = data_string + self.digits[i]

		data_string = data_string + ";"
		self.dev.write(data_string)
		#commands.getoutput("arduino-serial -b %d -p %s -s '%s'" % (self.speed, self.device, data_string))

	def setDigit(self, digit_number, value):
		self.digits[digit_number] = self.digit_dict[value]

	def clear(self):
		for i in xrange(len(self.digits)):
			self.digits[i] = '00'

	def setExtraLED(self, digit_number, status):
		self.extra_leds[digit_number] = status


if __name__ == '__main__':
  display = ArduinoDisplayLCD()
  time.sleep(2)
  old_num = 0
  while (True):
	  num = commands.getoutput("printf \"%4s\n\" \"$(uptime | grep -o 'load average: [^,]*' | cut -c15- | tr -d '.')\"")
	  if (num != old_num):
		  old_num = num
		  display.setDigit(0,num[0])
		  display.setDigit(1,num[1])
		  display.setDigit(2,num[2])
		  display.setDigit(3,num[3])
		  display.updateDisplay()
	  time.sleep(0.1)
  display.close()

