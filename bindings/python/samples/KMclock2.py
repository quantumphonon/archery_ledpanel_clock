from samplebase import SampleBase
from rgbmatrix import graphics
import time
import socketio
import threading

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global clock_time
        global clock_line
        global clock_color
        canvas = self.matrix
        font1 = graphics.Font()
        font1.LoadFont("../../../fonts/10x20.bdf")
        font2 = graphics.Font()
        font2.LoadFont("../../../fonts/7x13.bdf")
        green = graphics.Color(0, 255, 0)
        red = graphics.Color(255, 0, 0)
        yellow = graphics.Color(255, 255, 0)
        white = graphics.Color(255, 255, 255)
        black = graphics.Color(0,0,0)
        
        while True:
            if clock_line == 6:
                clock_line_text = 'CD'
            elif clock_line == 5:
                clock_line_text = 'AB'
            else:
                clock_line_text = ''
                
            if clock_color == 3:
                clock_color_output = green
                text_color = white
            elif clock_color == 2:
                clock_color_output = yellow
                text_color = black
            else:
                clock_color_output = red
                text_color = white
                
            
            for i in range(32):
                graphics.DrawLine(canvas, 0, i, 63, i, clock_color_output)
            graphics.DrawText(canvas, font1, 25, 15, text_color, str(clock_time))
            graphics.DrawText(canvas, font2, 25, 28, text_color, clock_line_text)    
            time.sleep(0.5)   # show display for 10 seconds before exit  

def graphics_test():
    draw_test = GraphicsTest()
    if (not draw_test.process()):
        draw_test.print_help()
def clock_server_connection():
    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.on('hornMessage')
    def on_messege(soundfile, outoftime):
        print('soundfile:', soundfile)
        print('outoftime:', outoftime)

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        global clock_time
        global clock_line
        global clock_color
        clock_time = time1
        clock_line = whoShoots
        clock_color = light1
        """
        print('time1:', time1)
        print('light1:', light1)
        print('time2:', time2)
        print('light2:', light2)
        print('beacon:', beacon)
        print('numbers:', numbers)
        print('whoShoots:', whoShoots)
        print('beep:', beep)
        print('led:', led)
        """

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
    clock_time = 0
    clock_color = 0
    clock_line = 0
    t1=threading.Thread(target=graphics_test)
    t2=threading.Thread(target=clock_server_connection)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    