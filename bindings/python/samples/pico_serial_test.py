import serial
from time import sleep

horn_controller = serial.Serial("COM3")

def get_temperature(serial_connection):
    command_string = f"checktemp:1\n".encode()
    serial_connection.write(command_string)
    response_string = serial_connection.readline()
    print(response_string)
    return "error"