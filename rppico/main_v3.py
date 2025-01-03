from machine import Pin, PWM
import sys
import time

led = Pin(15, Pin.OUT)
led2 = Pin(25, Pin.OUT)
led.value(0)
led2.value(0)

led_pwm = PWM(Pin(14))
led_pwm.freq (1000)
led_pwm.duty_u16(600)


while True:
    read_data = sys.stdin.readline().strip()
    
    beeps = int(read_data[0])
    if len(read_data)>1:
        pwm_value = int(read_data[2:])
        led_pwm.duty_u16(pwm_value)
    for i in range(beeps):
        led.toggle()
        led2.toggle()
        time.sleep(0.5)
        led.toggle()
        led2.toggle()
        time.sleep(0.5)
