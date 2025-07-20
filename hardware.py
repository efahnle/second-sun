import RPi.GPIO as GPIO
#import time
  


def init_gpio(gpio_pin:int) -> GPIO.PWM:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(gpio_pin, GPIO.OUT)
    light_gpio = GPIO.PWM(gpio_pin, 100)
    #light_gpio.start(100)  
    return light_gpio