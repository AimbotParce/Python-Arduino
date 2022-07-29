import python_arduino

placa = python_arduino.set_arduino_board(port='COM3')

placa.get_pin('d', 10, 'i')
placa.get_pin('d', 6, 'o')
placa.get_pin('a', 1, 'i')

while True:
    if placa.digital_read(10):
        value = int(255*placa.analog_read(1)/1023)
        print("{0} ".format(value), end='\r')
        placa.analog_write(6, value)
    else:
        print("OFF        ", end='\r')
        placa.digital_write(6, False)