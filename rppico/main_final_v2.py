from machine import Pin, PWM, ADC
import sys
import time

sound_levels = [58500, 59000, 59500, 61000, 62500, 65000]

temperature_pin = 4
sensor = ADC(temperature_pin)

def read_temperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

led = Pin(15, Pin.OUT)
led2 = Pin(25, Pin.OUT)
led.value(0)
led2.value(0)

soundlevel_pin_1 = Pin(10, Pin.IN, Pin.PULL_UP)
soundlevel_pin_2 = Pin(11, Pin.IN, Pin.PULL_UP)
soundlevel_pin_3 = Pin(12, Pin.IN, Pin.PULL_UP)
soundlevel_pin_4 = Pin(3, Pin.IN, Pin.PULL_UP)
soundlevel_pin_5 = Pin(4, Pin.IN, Pin.PULL_UP)
soundlevel_pin_6 = Pin(5, Pin.IN, Pin.PULL_UP)

soundlevel_pins = [soundlevel_pin_1,
                   soundlevel_pin_2,
                   soundlevel_pin_3,
                   soundlevel_pin_4,
                   soundlevel_pin_5,
                   soundlevel_pin_6]

def check_soundlevel(soundlevel_pins):
    for i in range(len(soundlevel_pins)):
        if soundlevel_pins[i].value() == 0:
            return i
        

brightness_pin_up = Pin(21, Pin.IN, Pin.PULL_UP)
brightness_pin_down = Pin(20, Pin.IN, Pin.PULL_UP)

def check_brightness_pins(pin_up, pin_down):
    if pin_up.value() == 0 and pin_down.value() == 0:
        return "both"
    elif pin_up.value() == 0 and pin_down.value() != 0:
        return "up"
    if pin_up.value() != 0 and pin_down.value() == 0:
        return "down"
    else:
        return "none"
    

led_pwm = PWM(Pin(14))
led_pwm.freq (10000)
led_pwm.duty_u16(45000)


while True:
    read_data = sys.stdin.readline().strip()
    read_data = read_data.split(":")
    command = read_data[0]
    value = read_data[1]
    
    if command == "checktemp":
        current_temperature = read_temperature()
        temperature_string = f"temp:{current_temperature}\n".encode()
        sys.stdout.write(temperature_string)
        
    if command == "horn":
        sound_level = check_soundlevel(soundlevel_pins)
        led_pwm.duty_u16(sound_levels[sound_level])
        response = f"horn:{sound_level}\n".encode()
        
        
        for i in range(int(value)):
            led.toggle()
            led2.toggle()
            time.sleep(0.5)
            led.toggle()
            led2.toggle()
            time.sleep(0.5)
            
    if command == "checkbrightness":
        pressed_buttons = check_brightness_pins(brightness_pin_up, brightness_pin_down)
        response = f"button:{pressed_buttons}\n".encode()
        sys.stdout.write(response)

