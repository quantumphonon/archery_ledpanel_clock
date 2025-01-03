from samplebase import SampleBase
from rgbmatrix import graphics
import time
import socketio
import threading
from queue import Queue
import serial
import requests

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global clock_time
        global clock_line
        global clock_color
        canvas = self.matrix
        font1 = graphics.Font()
        font1.LoadFont("../../../fonts/font_1rows.bdf")
        font2 = graphics.Font()
        font2.LoadFont("../../../fonts/finaltime.bdf")
        font3 = graphics.Font()
        font3.LoadFont("../../../fonts/font_3rows.bdf")
        green = graphics.Color(1, 255, 1)
        red = graphics.Color(255, 1, 1)
        yellow = graphics.Color(255, 255, 1)
        white = graphics.Color(255, 255, 255)
        black = graphics.Color(1,1,1)
        blue = graphics.Color(1, 1, 255)


        previous_score = {"type": "score",
                 "name1": "x",
                 "name2": "x",
                 "score1":"0",
                 "score2": "0",
                 "endscore1": "0",
                 "endscore2": "0",
                 "arrows1": "10",
                 "arrows2": "10"}
				 
        previous_time = {"type": "time",
        "time1": 0,
        "light1": 0,
        "time2": 0,
        "light2": 0,
        "beacon": 0,
        "numbers": 0,
        "whoShoots": 0,
        "beep": 0,
        "led": 0}


        for i in range(24*4):
            graphics.DrawLine(canvas, 96, i, 671, i, blue)

        while True:
            clock_state = state_queqe.get()

            if clock_state['type'] == 'time':
                if clock_state['whoShoots'] == 6:
                    clock_line_text = 'CD'
                elif clock_state['whoShoots'] == 5:
                    clock_line_text = 'AB'
                else:
                    clock_line_text = ''

                if clock_state['light1'] == 3:
                    clock_color_output_1 = green
                    text_color_1 = white
                elif clock_state['light1'] == 2:
                    clock_color_output_1 = yellow
                    text_color_1 = black
                else:
                    clock_color_output_1 = red
                    text_color_1 = white

                if clock_state['light2'] ==3:
                    clock_color_output_2 = green
                    text_color_2 = white
                elif clock_state['light2']==2:
                    clock_color_output_2 = yellow
                    text_color_2 = black
                else:
                    clock_color_output_2 = red
                    text_color_2 = white

                if clock_state['light1'] != previous_time['light1']:
                    for i in range(24*4):
                        graphics.DrawLine(canvas, 0, i, 95, i, clock_color_output_1)
                    graphics.DrawText(canvas, font2, 20-int(len(str(clock_state['time1']))*9/2), 70, text_color_1, str(clock_state['time1']))
                else:
                    if clock_state['time1'] != previous_time['time1']:
                        graphics.DrawText(canvas, font2, 20-int(len(str(previous_time['time1']))*9/2), 70, clock_color_output_1, str(previous_time['time1']))
                        graphics.DrawText(canvas, font2, 20-int(len(str(clock_state['time1']))*9/2), 70, text_color_1, str(clock_state['time1']))

                if clock_state['light2'] != previous_time['light2']:
                    for i in range(4*24):
                        graphics.DrawLine(canvas, 672, i ,767, i, clock_color_output_2)
                    graphics.DrawText(canvas, font2, 720-24+12-int(len(str(clock_state['time2']))*9/2), 70, text_color_2, str(clock_state['time2']))
                else:
                    if clock_state['time2'] != previous_time['time2']:
                        graphics.DrawText(canvas, font2, 720-24+12-int(len(str(previous_time['time2']))*9/2), 70, clock_color_output_2, str(previous_time['time2']))
                        graphics.DrawText(canvas, font2, 720-24+12-int(len(str(clock_state['time2']))*9/2), 70, text_color_2, str(clock_state['time2']))


                previous_time=clock_state


            elif clock_state['type'] == 'score':

                graphics.DrawText(canvas, font1, 106, 30, blue, previous_score['name1'])
                graphics.DrawText(canvas, font1, 106, 30, white, clock_state['name1'])
                graphics.DrawText(canvas, font1, 671+20-26*len(previous_score['name2']), 30, blue, previous_score['name2'])
                graphics.DrawText(canvas, font1, 671+20-26*len(clock_state['name2']), 30, white, clock_state['name2'])
                graphics.DrawText(canvas, font1, 108, 93, blue, "Set:"+previous_score['endscore1'])
                graphics.DrawText(canvas, font1, 108, 93, white, "Set:"+clock_state['endscore1'])
                graphics.DrawText(canvas, font1, 394, 93, blue, "Set:"+previous_score['endscore2'])
                graphics.DrawText(canvas, font1, 394, 93, white, "Set:"+clock_state['endscore2'])
                graphics.DrawText(canvas, font1, 106+144, 93, blue, "Tot:"+previous_score['score1'])
                graphics.DrawText(canvas, font1, 106+144, 93, white, "Tot:"+clock_state['score1'])
                graphics.DrawText(canvas, font1, 394 + 144, 93, blue, "Tot:"+previous_score['score2'])
                graphics.DrawText(canvas, font1, 394 + 144, 93, white, "Tot:"+clock_state['score2'])
                arrows1 = previous_score['arrows1'].split(" ")

            for i in range(len(arrows1)):
                graphics.DrawText(canvas, font1, 106 + i * 64, 60, blue, arrows1[i])
                arrows1 = clock_state['arrows1'].split(" ")
                for i in range(len(arrows1)):
                    graphics.DrawText(canvas, font1, 106 + i * 64, 60, white, arrows1[i])
                arrows2 = previous_score['arrows2'].split(" ")
                for i in range(len(arrows2)):
                    graphics.DrawText(canvas, font1, 671-192 + i * 64, 60, blue, arrows2[i])
                arrows2 = clock_state['arrows2'].split(" ")
                for i in range(len(arrows2)):
                    graphics.DrawText(canvas, font1, 671-192 + i * 64, 60, white, arrows2[i])
                previous_score = clock_state

def graphics_test():
    draw_test = GraphicsTest()
    if (not draw_test.process()):
        draw_test.print_help()

def get_match_data():
    while True:
        data = requests.get('http://192.168.2.5/Modules/Custom/IanseoGrafikiVideo/IanseoPresentationLED.php?tour=24SZY')
        data = data.content.decode('utf-8')
        data = data.replace("<br />","").splitlines()
        print(data)
        score = {"type": "score",
                 "name1": data[0],
                 "name2": data[4],
                 "score1": data[3],
                 "score2": data[7],
                 "endscore1": data[2],
                 "endscore2": data[6],
                 "arrows1": data[1],
                 "arrows2": data[5]}
        state_queqe.put(score)
        time.sleep(1)


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
        time_string = f"{soundfile}\n".encode()
        horn_controller.write(time_string)

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        new_state = {"type": "time",
                    "time1": time1,
                    "light1": light1,
                    "time2": time2,
                    "light2": light2,
                    "beacon": beacon,
                    "numbers": numbers,
                    "whoShoots": whoShoots,
                    "beep": beep,
                    "led": led}
        #print(new_state)
        state_queqe.put(new_state)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://192.168.2.5:5001')
    sio.wait()
"""
#
#t1 = threading.Thread(target=sio.wait)
#t2 = threading.Thread(target=graphics_test)
"""
# Main function
if __name__ == "__main__":
    initial_time = {"type": "time",
                    "time1": 0,
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
    t3=threading.Thread(target=get_match_data)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
