#!/usr/bin/env python

# dbus imports
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

# arduino imports
from arduino7seg import ArduinoDisplayLCD

class MyDbusObject(dbus.service.Object):
	def __init__(self, session_bus, object_path):
		self.display = ArduinoDisplayLCD()
		dbus.service.Object.__init__(self, session_bus, object_path)

	@dbus.service.method("LEDs.Display",
				in_signature='', out_signature='')
	def clear(self):
		self.display.clear()

	@dbus.service.method("LEDs.Display",
				in_signature='is', out_signature='')
	def setDigit(self, digit_number, value):
		self.display.setDigit(digit_number, value[0])

	@dbus.service.method("LEDs.Display",
				in_signature='is', out_signature='')
	def set2Digits(self, couple_number, value):
		if (len(value) == 0): value = '  '
		if (len(value) == 1): value = ' ' + value
		self.display.setDigit(couple_number, value[0])
		self.display.setDigit(couple_number+1, value[1])

	@dbus.service.method("LEDs.Display",
				in_signature='s', out_signature='')
	def set4Digits(self, value):
		if (len(value) == 0): value = '    '
		if (len(value) == 1): value = '   ' + value
		if (len(value) == 2): value = '  ' + value
		if (len(value) == 3): value = ' ' + value

		for i in range(4):
			self.display.setDigit(i, value[i])

	@dbus.service.method("LEDs.Display",
				in_signature='ii', out_signature='')
	def setExtraLED(self, digit_number, status):
		if (status == 0):
			self.display.setExtraLED(digit_number, False)
		else:
			self.display.setExtraLED(digit_number, True)

	@dbus.service.method("LEDs.Display",
				in_signature='', out_signature='')
	def updateDisplay(self):
		self.display.updateDisplay()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	session_bus = dbus.SessionBus()
	name = dbus.service.BusName("MyStuff.LCD", session_bus)
	object = MyDbusObject(session_bus, '/')

	mainloop = gobject.MainLoop()
	mainloop.run()
