Arduino 7seg
============

About
-----
A tiny project that I've done at 2009 for controlling a 7 segment LED Display (from an old microwave oven) from a PC, using Arduino.

[Youtube video](https://www.youtube.com/watch?v=_u9xNM2KU-A).


Software Components
-------------------
Bash (DBUS_client) -> DBUS service -> python library -> Arduino


Files
-----
- code/arduino/7seg.pde - Arduino code.
- code/linux/arduino7seg.py - Python library for 7seg control.
- code/linux/arduino7seg_dbus.py - DBUS service.
- 7seg - Bash CLI tool.
- doc/7seg.fz - schematics (can be opened using [fritzing](http://fritzing.org/)).

Schematics
----------
![schema](https://raw.githubusercontent.com/nadavh/arduino_7seg/master/doc/img/7seg.png)
![picture](https://raw.githubusercontent.com/nadavh/arduino_7seg/master/doc/img/arduino-lcd.png)
