"""
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#no usar 19, no adna
GPIO.setup(16, GPIO.OUT)
rojo = GPIO.PWM(16, 100)
rojo.start(100)    

while True:
    try:
        for i in range(100,-1,-1):
            rojo.ChangeDutyCycle(i)
            time.sleep(0.02)           
    
        for i in range(100,-1,-1):
            rojo.ChangeDutyCycle(100 - i)
            time.sleep(0.02)           
        print("Ciclo completo")
    except KeyboardInterrupt as e:
        rojo.ChangeDutyCycle(0)
        print("sali")
        GPIO.cleanup()
        raise e
"""

from config import load_config
from hardware import init_gpio

def main():
    config = load_config()
    if config:
        print(f"Configuration loaded successfully: {config}")
        #print(config)
    else:
        print("Failed to load configuration.")
        exit(1)

    light = init_gpio(config.get('gpio_pin', 16))
    print(light)


if __name__ == "__main__":
    main()