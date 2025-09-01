import RPi.GPIO as GPIO
from light_to_use import get_light_to_use


def init_gpio(gpio_pin: int) -> GPIO.PWM:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gpio_pin, GPIO.OUT)
    light_gpio = GPIO.PWM(gpio_pin, 100)
    light_gpio.start(0)

    return light_gpio


def cleanup() -> None:
    GPIO.cleanup()
    print("GPIO cleaned up.")


def change_light_brightness(lamp: GPIO.PWM, days: dict) -> None:
    brightness = get_light_to_use(days)
    if not hasattr(change_light_brightness, 'last_brightness') or change_light_brightness.last_brightness != brightness:
        lamp.ChangeDutyCycle(brightness)
        change_light_brightness.last_brightness = brightness
