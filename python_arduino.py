# Arduino controller for python, by Marc Parcerisa

from __future__ import annotations
from typing import Union
import serial
import time

class set_arduino_board:
    def __init__(self, port: str = 'COM3', setup_time: float = 2.0) -> set_arduino_board:
        """
        Gets the configuration from the board connected to the specified port (default: COM3), and initialitzates the library.
        setup_time is the time this function assumes the serial needs to be set (default: 2 seconds).
        """
        print(f"Setting up serial in port {port}...")
        self.ser = serial.Serial(port, timeout = 5)
        time.sleep(setup_time)
        # print("Port should now be set! Getting board configuration...")
        self.ser.write(bytes([1]))  #PY_GET_BOARD
        self.firstAnalog = int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        assert self.firstAnalog != b'', "Something went wrong during the board setup, most likely the serial didnt have enough time to setup, try adding setup_time"
        # print(f"Recieved: {self.firstAnalog}")
        print("Set! Welcome to the Python controller for Arduino!")

        self.availablePins = {}

    def get_pin(self, pinType: Union[int, str], pinNumber: int, pinMode: Union[int, str]) -> int:
        """
        Sets the given pin as the given mode. The type and mode should be given in a string (or integer):
        'd' (or 0) for digital, 'a' (or 1) for analog; and 'o' (or 0) for output, 'i' (or 1) for input.
        """
        self.ser.write(bytes([2]))  #PY_GET_PIN

        stringMapping = {'d':0, 'a':1, 'o':0, 'i':1}
        if type(pinType) == str:
            pinType = stringMapping[pinType]
        if type(pinMode) == str:
            pinMode = stringMapping[pinMode]

        if pinType == 1:
            pinNumber += self.firstAnalog
        
        

        self.ser.write(bytes([pinNumber]))
        self.ser.write(bytes([pinMode]))
        self.availablePins[pinNumber] = pinMode
        exitCode = int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        assert exitCode == 0, "Something went wrong while setting the pin on the arduino board"
        return exitCode

    def get_pin_reference(self, pinType: Union[int, str], pinNumber: int) -> int:
        """
        Returns the pin integer reference, for future uses. pinType must be 'd' (or 0) for digital pins and 'a' (or 1) for analog ones.
        """
        stringMapping = {'d':0, 'a':1}
        if type(pinType) == str:
            pinType = stringMapping[pinType]
        if pinType == 1:
            pinNumber += self.firstAnalog
        return pinNumber

    def digital_write(self, pin: int, value: bool, pinType: Union[int, str] = 'd') -> int:
        """
        Writes the given value to the given digital pin (1/True for HIGH, 0/False for LOW).
        Remember you can reference analog pins by its integer reference (for example: A0 could be pin 14)
        or by changing the pinType (digital ('d' or 0), as default, or analog ('a' or 1))).
        get_pin_reference() function returns the pin integer reference if you need it.

        Returns an exit code: 0 - Everything okay, 1 - An error ocurred
        """
        assert pin in self.availablePins , "The given pin isn't initialized yet"
        self.ser.write(bytes([3])) #PY_DIGITAL_WRITE

        stringMapping = {'d':0, 'a':1}
        if type(pinType) == str:
            pinType = stringMapping[pinType]
        if pinType == 1:
            pin += self.firstAnalog

        self.ser.write(bytes([pin]))
        if value:
            value = 1
        else:
            value = 0
        self.ser.write(bytes([value]))
        try:
            return int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 1

    def analog_read(self, analogPin: int) -> float:
        """
        Returns a floating point between 0 and 1023 given by the read value from the given pin. Remember the pinNumber would be 0 for A0, 1 for A1...
        """
        assert (analogPin+self.firstAnalog) in self.availablePins, "The given pin isn't initialized yet"
        self.ser.write(bytes([4]))  #PY_ANALOG_READ

        self.ser.write(bytes([analogPin]))
        try:
            return float(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 0

    def digital_read(self, digitalPin: int, pinType: Union[int, str] = 'd') -> bool:
        """
        Returns a boolean value given by the digital read from the given pin. Remember you can read from analog pins
        by giving its integer reference, or by changing the pinType ('d' or 0 for digital, as default, and 'a' or 1 for analaog)
        """
        stringMapping = {'d':0, 'a':1}
        if type(pinType) == str:
            pinType = stringMapping[pinType]
        if pinType == 1:
            digitalPin += self.firstAnalog
        assert digitalPin in self.availablePins, "The given pin isn't initialized yet"
        self.ser.write(bytes([5]))  #PY_DIGITAL_READ
        self.ser.write(bytes([digitalPin]))
        
        try:
            return int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8")) == 1
        except:
            return 0
    
    def analog_write(self, pin: int, value: int) -> int:
        """
        Writes the desired value into the given digital pin. The value must be between 0 and 255.

        Returns an exit code: 0 - Everything okay, 1 - An error ocurred
        """
        assert pin in self.availablePins, "The given pin isn't initialized yet"
        assert type(value) == int, "The given value must be an integer"
        assert (value >= 0 and value <= 255), "The given value must be between 0 and 255"
        self.ser.write(bytes([6]))  #PY_ANALOG_WRITE

        self.ser.write(bytes([pin]))
        self.ser.write(bytes([value]))

        try:
            return int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 0
    
    def pulse_in(self, pin: int, value: bool, pinType: Union[int, str] ='d') -> float:
        """
        Reads a pulse (either HIGH or LOW) on a pin. For example, if value is HIGH (True), pulse_in() waits for the pin to go from LOW to HIGH,
        starts timing, then waits for the pin to go LOW and stops timing. Returns the length of the pulse in microseconds.

        If you want to read a pulse from an analog pin, you can change the pinType to 'a' (or 1)
        """
        stringMapping = {'d':0, 'a':1}
        if type(pinType) == str:
            pinType = stringMapping[pinType]
        if pinType == 1:
            pin += self.firstAnalog

        assert pin in self.availablePins, "The given pin isn't initialized yet"
        assert type(value) == bool, "The given value must be either True (HIGH) or False (LOW)"
        self.ser.write(bytes([7]))  #PY_PULSE_IN

        self.ser.write(bytes([pin]))
        if value:
            value = 1
        else:
            value = 0
        self.ser.write(bytes([value]))

        try:
            return float(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 0

    def tone(self, pin: int, frequency: int, duration: int = 0) -> int:
        """
        Generates a square wave of the specified frequency on a digital pin (only those with a tilda written on the board).
        A duration can be specified (in milliseconds), otherwise the wave continues until a call to noTone().
        It is not possible to generate tones lower than 31Hz.

        Returns an exit code: 0 - Everything okay, 1 - An error ocurred
        """
        assert pin in self.availablePins, "The given pin isn't initialized yet"
        self.ser.write(bytes([8]))  #PY_TONE

        self.ser.write(bytes([pin]))
        self.ser.write((str(frequency) + '\n').encode())
        self.ser.write((str(duration) + '\n').encode())

        try:
            return int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 1

    def no_tone(self, pin: int) -> int:
        """
        Stops a tone from playing in the specified pin.

        Returns an exit code: 0 - Everything okay, 1 - An error ocurred
        """
        assert pin in self.availablePins, "The given pin isn't initialized yet"
        self.ser.write(bytes([9]))  #PY_NO_TONE
        self.ser.write(bytes([pin]))

        try:
            return int(self.ser.read_until(b'\n').strip(b'\r\n').decode("utf-8"))
        except:
            return 1

if __name__ == '__main__':
    arduinoBoard = set_arduino_board(port = 'COM3')
    arduinoBoard.get_pin('d', 6, 'o')  #LED
    arduinoBoard.get_pin('a', 1, 'i')  #Potenciometro
    arduinoBoard.get_pin('d', 10, 'i') #Botón
    while True:
        potencia = int(255*arduinoBoard.analog_read(1)/1023)
        if arduinoBoard.digital_read(10):
            arduinoBoard.analog_write(6, potencia)
        else:
            arduinoBoard.analog_write(6, 0)
