import time
import threading
from queue import Queue
import serial
import socketio


def clock_server_connection():
    #horn_controller = serial.Serial('COM3')

    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.on('hornMessage')
    def on_messege(soundfile, outoftime):
        print('soundfile:', soundfile)
        print('outoftime:', outoftime)
        #horn_controller.write(str(soundfile).encode())

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        print(time1)
        new_state = {"time1": time1,
                    "light1": light1,
                    "time2": time2,
                    "light2": light2,
                    "beacon": beacon,
                    "numbers": numbers,
                    "whoShoots": whoShoots,
                    "beep": beep,
                    "led": led}
        #state_queqe.put(new_state)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://192.168.0.101:5001')
    sio.wait()
"""
#
#t1 = threading.Thread(target=sio.wait)
#t2 = threading.Thread(target=graphics_test)
"""
# Main function
if __name__ == "__main__":
    initial_time = {"time1": 0,
                    "light1": 0,
                    "time2": 0,
                    "light2": 0,
                    "beacon": 0,
                    "numbers": 0,
                    "whoShoots": 0,
                    "beep": 0,
                    "led": 0}
    state_queqe = Queue()
    state_queqe.put(initial_time)

    t2=threading.Thread(target=clock_server_connection)
    t2.start()
    t2.join()


