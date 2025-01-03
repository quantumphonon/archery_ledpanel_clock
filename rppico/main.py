from machine import Pin, PWM
import sys
import time

led = Pin(15, Pin.OUT)
led2 = Pin(25, Pin.OUT)
led.value(0)
led2.value(0)
ledpwm = Pin(20)
led_pwm = PWM(ledpwm)
led_pwm.freq (1000)
led_pwm.duty_u16(10000)

while True:
    read_data = sys.stdin.readline().strip()
    
    beeps = int(read_data[0])
    for i in range(beeps):
        led.toggle()
        led2.toggle()
        time.sleep(0.5)
        led.toggle()
        led2.toggle()
        time.sleep(0.5)
