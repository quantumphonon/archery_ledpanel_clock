from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import numpy
import socketio
import clockconfig

def main():
    # screen parameters
    size = clockconfig.clocksize

    # fonts loading
    font_time_small = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 60)
    font_time_big = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 90)
    font_line = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 30)
    fonts = {"font_time_small": font_time_small,
             "font_time_big": font_time_big,
             "font_line": font_line}

    default_image = Image.open('./bindings/python/samples/default_logo.png')

    # example data
    line_code = 6
    time = "10"
    background_code = 2

    # program
    options = RGBMatrixOptions()
    options.rows = clockconfig.led_rows
    options.cols = clockconfig.led_cols
    options.chain_length = clockconfig.led_chain
    options.parallel = clockconfig.led_parallel
    options.brightness = clockconfig.led_brightness
    options.pixel_mapper_config = clockconfig.led_pixel_mapper
    options.gpio_slowdown = clockconfig.led_slowdown_gpio
    options.multiplexing = clockconfig.led_multiplexing

    matrix = RGBMatrix(options = options)
    matrix.SetImage(default_image.convert('RGB'))

    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.on('timeMessage')
    def on_message(time1, light1, time2, light2, beacon, numbers, whoShoots, beep, led):
        """
        print({"time1": time1
               , "time2": time2
               , "light1": light1
               , "light2": light2
               , "beacon": beacon
               , "numbers": numbers
               , "whoShoots": whoShoots
               , "beep": beep
               , "led": led
               })
        """
        if light1 > 3:
            matrix.SetImage(default_image.convert('RGB'))

        if clockconfig.if_clock_left:
            time = time1
            background_code = light1
        else:
            time = time2
            background_code = light2

        clock_image = generate_clock_image(size, time, background_code, whoShoots, fonts)
        matrix.SetImage(clock_image.convert('RGB'))
        
    @sio.on('hornMessage')
    def on_messege(soundfile, outoftime):
        pass

    sio.connect('http://' + clockconfig.ip_clocksystem + ':5001')
    sio.wait()

def generate_clock_image(screen_size, time, background_code, whoShoots, fonts):
    background_color, text_color = color_code_to_color(background_code)

    clock_image = Image.fromarray(numpy.full((screen_size[0], screen_size[1], 3), background_color, dtype=numpy.uint8))
    image_with_text = ImageDraw.Draw(clock_image)

    line_text = line_code_to_text(whoShoots)
    if line_text:
        font_time = fonts['font_time_small']
        line_text_width = image_with_text.textlength(line_text, font=fonts['font_line]'])
        image_with_text.text((int((screen_size[1]-line_text_width)/2),66), line_text, font=fonts['font_line]'], fill=text_color)
    else:
        font_time = fonts['font_time_big']

    time = str(time)
    time_width = image_with_text.textlength(time, font=font_time)
    image_with_text.text((int((screen_size[1]-time_width)/2),2), time, font=font_time, fill=text_color)
    return clock_image

def line_code_to_text(line_code):
    if line_code == 5:
        return "AB"
    elif line_code == 6:
        return "CD"
    return ""


def color_code_to_color(color_code):
    if color_code == 2:
        yellow = (255, 255, 0)
        black = (0,0,0)
        return yellow, black
    elif color_code == 3:
        green = (0,128,0)
        white = (255,255,255)
        return green, white
    red = (255,0,0)
    white = (255,255,255)
    return red, white
    

if __name__ == "__main__":
    main()