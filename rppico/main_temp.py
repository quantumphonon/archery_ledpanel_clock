from machine import Pin, PWM, ADC
import sys
import time

temperature_pin = 4
sensor = ADC(temperature_pin)

def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

led = Pin(15, Pin.OUT)
led2 = Pin(25, Pin.OUT)
led.value(1)
led2.value(0)

led_pwm = PWM(Pin(14))
led_pwm.freq (10000)
led_pwm.duty_u16(600)


while True:
    read_data = sys.stdin.readline().strip()
    read_data = read_data.split(":")
    command = read_data[0]
    value = read_data[1]
    if command == "checktemp":
        current_temperature = ReadTemperature()
        temperature_string = f"temp:{current_temperature}\n".encode()
        sys.stdout.write(temperature_string)
        
    if command == "horn":
        for i in range(int(value)):
            led.toggle()
            led2.toggle()
            time.sleep(0.5)
            led.toggle()
            led2.toggle()
            time.sleep(0.5)