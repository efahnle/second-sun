import RPi.GPIO as GPIO
from light_to_use import get_light_to_use
from utils import log


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


# Global variable to share brightness with prometheus exporter
current_brightness = 0.0

def change_light_brightness(lamp: GPIO.PWM, days: dict) -> None:
    global current_brightness
    brightness = get_light_to_use(days)
    
    # Only change if different from last brightness
    if not hasattr(change_light_brightness, 'last_brightness'):
        change_light_brightness.last_brightness = 0.0
    
    if abs(brightness - change_light_brightness.last_brightness) > 0.01:  # Only update if >0.01% difference
        log(f"PWM: Changing brightness from {change_light_brightness.last_brightness:.2f}% to {brightness:.2f}%")
        lamp.ChangeDutyCycle(brightness)
        change_light_brightness.last_brightness = brightness
    
    current_brightness = brightness
