from samplebase import SampleBase
from rgbmatrix import graphics
import time
import socketio
import threading
from queue import Queue
import serial

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global clock_time
        global clock_line
        global clock_color
        canvas = self.matrix
        font1 = graphics.Font()
        font1.LoadFont("fonts/font_1rows.bdf")
        font2 = graphics.Font()
        font2.LoadFont("fonts/font_2rows.bdf")
        font3 = graphics.Font()
        font3.LoadFont("fonts/font_3rows.bdf")
        green = graphics.Color(0, 140, 0)
        red = graphics.Color(255, 0, 0)
        yellow = graphics.Color(255, 255, 0)
        white = graphics.Color(255, 255, 255)
        black = graphics.Color(0,0,0)

        while True:
            clock_state = state_queqe.get()

            if clock_state['whoShoots'] == 6:
                clock_line_text = 'CD'
            elif clock_state['whoShoots'] == 5:
                clock_line_text = 'AB'
            else:
                clock_line_text = ''

            if clock_state['light1'] == 3:
                clock_color_output = green
                text_color = white
            elif clock_state['light1'] == 2:
                clock_color_output = yellow
                text_color = black
            else:
                clock_color_output = red
                text_color = white


            for i in range(96):
                graphics.DrawLine(canvas, 0, i, 191, i, clock_color_output)

            if len(clock_line_text)>0:
                font_time = font2
                time_location = 62
                shift_per_letter = 26
                graphics.DrawText(canvas, font1, 66, 94, text_color, clock_line_text)
            else:
                font_time = font3
                time_location = 80
                shift_per_letter = 30
            graphics.DrawText(canvas, font_time, 96-int(len(str(clock_state['time1']))*shift_per_letter), time_location, text_color, str(clock_state['time1']))

def graphics_test():
    draw_test = GraphicsTest()
    if (not draw_test.process()):
        draw_test.print_help()


def clock_server_connection():
    horn_controller = serial.Serial('/dev/ttyACM0')
    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')

    @sio.on('hornMessage')
    def on_messege(soundfile, outoftime):
        print('soundfile:', soundfile)
        print('outoftime:', outoftime)
        time_string = f"{soundfile} 60000\n".encode()
        horn_controller.write(time_string)

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        new_state = {"time1": time1,
                    "light1": light1,
                    "time2": time2,
                    "light2": light2,
                    "beacon": beacon,
                    "numbers": numbers,
                    "whoShoots": whoShoots,
                    "beep": beep,
                    "led": led}
        state_queqe.put(new_state)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://192.168.0.11:5001')
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

    t1=threading.Thread(target=graphics_test)
    t2=threading.Thread(target=clock_server_connection)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
