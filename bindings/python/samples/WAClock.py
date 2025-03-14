from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import numpy
import socketio
import clockconfig
import serial
import time
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('clockconfig.ini')

    # screen parameters
    size = (int(config['Display']['clocksize_y']), int(config['Display']['clocksize_x']))

    # fonts loading
    font_time_small = ImageFont.truetype("ARIALBD.TTF", 84)
    font_time_big = ImageFont.truetype("ARIALBD.TTF", 90)
    font_line = ImageFont.truetype("ARIALBD.TTF", 36)
    font_info = ImageFont.truetype("ARIAL.TTF", 14)
    fonts = {"font_time_small": font_time_small,
             "font_time_big": font_time_big,
             "font_line": font_line,
             "font_info": font_info}

    default_image = Image.open('default_logo.png')

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
    matrix.SetImage(default_image.convert('RGB'))

    # pico connection
    horn_controller = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0')

    current_clock_state = ClockState()
    print(current_clock_state.last_update_time)

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
        if light1 > 3 and light2 > 3:
            temp_image = default_image
            clear_info_image(temp_image)
            button_input = check_button_input(horn_controller)

            previous_input, last_update_time = process_button_input(config, matrix, button_input, current_clock_state.last_update_time, current_clock_state.previous_input)
            current_clock_state.previous_input = previous_input
            current_clock_state.last_update_time = last_update_time
            if time.time() - last_update_time < 5:
                current_temperature = get_temperature(horn_controller)
                add_temerature_info(current_temperature, temp_image, fonts)
                add_brightness_info(matrix.brightness, temp_image, fonts)
            if previous_input == "save":
                pass
                current_clock_state.config_save_time = last_update_time
            if time.time() - current_clock_state.config_save_time < 2:
                add_save_info(temp_image, fonts)

            matrix.SetImage(temp_image.convert('RGB'))
        else:
            if clockconfig.if_clock_left:
                clock_time = time1
                background_code = light1
            else:
                clock_time = time2
                background_code = light2

            clock_image = generate_clock_image(size, clock_time, background_code, whoShoots, fonts)
            matrix.SetImage(clock_image.convert('RGB'))

    @sio.on('hornMessage')
    def on_messege(soundfile, outoftime):
        time_string = f"horn:{soundfile}\n".encode()
        horn_controller.write(time_string)
        # response = horn_controller.readline().strip()
        # print(response)


    sio.connect('http://' + config['ClockSystem']['ip_clock'] + ':5001')
    sio.wait()

def generate_clock_image(screen_size, clock_time, background_code, whoShoots, fonts):
    background_color, text_color = color_code_to_color(background_code)

    clock_image = Image.fromarray(numpy.full((screen_size[0], screen_size[1], 3), background_color, dtype=numpy.uint8))
    image_with_text = ImageDraw.Draw(clock_image)

    line_text = line_code_to_text(whoShoots)
    if line_text:
        font_time = fonts['font_time_small']
        line_text_width = image_with_text.textlength(line_text, font=fonts['font_line'])
        image_with_text.text((int((screen_size[1]-line_text_width)/2),61), line_text, font=fonts['font_line'], fill=text_color)
        time_start_position_y = -12
    else:
        font_time = fonts['font_time_big']
        time_start_position_y = 0
    clock_time = str(clock_time)
    time_width = image_with_text.textlength(clock_time, font=font_time)
    image_with_text.text((int((screen_size[1]-time_width)/2), time_start_position_y), clock_time, font=font_time, fill=text_color)
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

def clear_info_image(image):
    image_cleared = ImageDraw.Draw(image)
    image_cleared.rectangle([(0,0),(191,24)],fill=(0,0,0))
    image_cleared.rectangle([(0,72),(191,95)],fill=(0,0,0))
    return None


def get_temperature(serial_connection):
    command_string = f"checktemp:1\n".encode()
    serial_connection.write(command_string)
    response_string = serial_connection.readline()
    temperature = response_string.decode('utf-8').strip()
    return temperature


def add_temerature_info(temperature, image, fonts):
    image_with_text = ImageDraw.Draw(image)
    text_location = (10,0)
    image_with_text.text(text_location, str(temperature) , font=fonts['font_info'], fill=(255,255,255))
    return None


def add_brightness_info(brightness, image, fonts):
    image_with_text = ImageDraw.Draw(image)
    text_location = (10,74)
    image_with_text.text(text_location, str(brightness) , font=fonts['font_info'], fill=(255,255,255))
    return None


def add_save_info(image, fonts):
    image_with_text = ImageDraw.Draw(image)
    text_location = (74,74)
    image_with_text.text(text_location, "save", font=fonts['font_info'], fill=(255,255,255))
    return None


def check_brightness_change(serial_connection):
    command_string = f"brightness_change:1".encode()
    serial_connection.write(command_string)
    response_string = serial_connection.readline().decode('utf-8').strip()
    return response_string


def check_button_input(serial_connection):
    command_string = f"checkbrightness:1\n".encode()
    serial_connection.write(command_string)
    for i in range(10):
        response_string = serial_connection.readline().decode('utf-8').strip()
        try:
            splitted_response = response_string.split(':')
            response = splitted_response[0]
            if response == 'button':
                return splitted_response[1]
        except IndexError:
            continue

def process_button_input(config, matrix, button_input, last_update_time, previous_button):
    current_time = time.time()
    if previous_button != button_input:
        last_update_time = current_time
    if button_input == "up" and (current_time - last_update_time) > 0.5:
        matrix.brightness = brightness_new_value(matrix.brightness, True)
        last_update_time = current_time
    elif button_input == "down" and (current_time - last_update_time) > 0.5:
        matrix.brightness = brightness_new_value(matrix.brightness, False)
        last_update_time = current_time
    elif button_input == "both" and (current_time - last_update_time) > 2:
        config['Display']['led_brightness'] = str(matrix.brightness)
        with open('clockconfig.ini', "w") as file:
            config.write(file)
        last_update_time = current_time
        button_input = "save"
    return button_input, last_update_time


def brightness_new_value(current_brightness, if_change_up):
    # list of available brightness to choose by user
    allowable_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
    allowable_values = numpy.array(allowable_values)
    closest_element_index = (numpy.abs(allowable_values - current_brightness)).argmin()
    if if_change_up:
        if closest_element_index < (len(allowable_values) - 1):
            return allowable_values[closest_element_index+1]
        else:
            return allowable_values[closest_element_index]
    else:
        if closest_element_index > 0:
            return allowable_values[closest_element_index - 1]
        else:
            return allowable_values[0]


class ClockState:
    def __init__(self):
        self.last_update_time = time.time()
        self.config_save_time = time.time()-2
        self.previous_input = "none"

if __name__ == "__main__":
    main()
