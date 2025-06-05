from rgbmatrix import RGBMatrix, RGBMatrixOptions
import parameters_ledclockforfinal as parameters
import WAFinalClock_funtioncs as finaloutput
from PIL import Image, ImageDraw, ImageFont
import numpy
import socketio
import clockconfig
import serial
import time
import configparser
import queue
import requests
import threading

q = queue.Queue()

config = configparser.ConfigParser()
config.read('clockconfig.ini')

# pico connection
horn_controller = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0')

# screen parameters
size = (int(config['Display']['clocksize_y']), int(config['Display']['clocksize_x']))


# example data
line_code = 6
clock_time = "10"
background_code = 2

# program
options = RGBMatrixOptions()
options.rows = int(config['Display']['led_rows'])
options.cols = int(config['Display']['led_cols'])
options.chain_length = int(config['Display']['led_chain'])
options.parallel = int(config['Display']['led_parallel'])
options.brightness = int(config['Display']['led_brightness'])
options.pixel_mapper_config = config['Display']['led_pixel_mapper']
options.gpio_slowdown = int(config['Display']['led_slowdown_gpio'])
options.multiplexing = int(config['Display']['led_multiplexing'])
options.pwm_lsb_nanoseconds = 130
options.pwm_bits = 11
matrix = RGBMatrix(options = options)

def main():
    t1=threading.Thread(target=final_display)
    t2=threading.Thread(target=read_time_signal)
    t3=threading.Thread(target=read_scores)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

def final_display():
    final_clock = finaloutput.ClockForFinals(parameters.screen_width, parameters.screen_height, matrix, config['Display']['clock_id'])
    while True:
        data = q.get()
        match data['datatype']:
            case 'time':
                if data['data'] != final_clock.time:
                    final_clock.update_timing(data['data'])
            case 'score':
                if data['data'] != final_clock.score:
                    final_clock.update_scores(data['data'])
            case _:
                pass

def read_time_signal():
    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        time_data = {"time1": time1,
                    "light1": light1,
                    "time2": time2,
                    "light2": light2
                    }
        q.put({"datatype": "time",
               "data": time_data})
    def on_messege(soundfile, outoftime):
        time_string = f"horn:{soundfile}\n".encode()
        horn_controller.write(time_string)


    sio.connect('http://' + config['ClockSystem']['ip_clock'] + ':5001')
    sio.wait()


def read_scores():
    while True:
        response = requests.get('http://localhost/Modules/Custom/IanseoGrafikiVideo/IanseoPresentationLED_json.php')
        if response.status_code == 500:
            scores = {'live': 0}
        else:
            scores = response.json()
            scores['live']=1
        q.put({'datatype': 'score',
            'data': scores})
        time.sleep(1)


if __name__ == "__main__":
    main()