# Python Arduino
 This is both a Python library and an Arduino program that lets you controll an Arduino board via intuitive Python functions. Makes Arduino feel like an I/O board for yor personal computer.
 
 To make it work, you just have to compile and run the program "Arduino_Firmware.ino" on your board. Then import the library on your Python code and initialize it by defining a new variable that will represent your board. It is important to pass the COM port as a `str` argument when initializing it, as the following:
 
 ```py
 import python_arduino
 
 board = python_arduino.set_arduino_board(port='COM3')
 ```
