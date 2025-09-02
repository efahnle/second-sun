import pigpio
from light_to_use import get_light_to_use
from utils import log


def init_gpio(gpio_pin: int) -> tuple:
    pi = pigpio.pi()
    if not pi.connected:
        log("Failed to connect to pigpio daemon")
        raise RuntimeError("pigpio connection failed")

    # Set hardware PWM: pin, frequency, duty_cycle (0-1000000)
    pi.hardware_PWM(gpio_pin, 1000, 0)  # 1kHz, 0% duty cycle
    log(f"Hardware PWM initialized on pin {gpio_pin} at 1000Hz", "DEBUG")

    return (pi, gpio_pin)


def cleanup(pi_instance=None) -> None:
    if pi_instance:
        pi_instance.stop()
    log("pigpio cleaned up.")


# Global variable to share brightness with prometheus exporter
current_brightness = 0.0


def change_light_brightness(lamp_info: tuple, days: dict) -> None:
    global current_brightness
    pi, gpio_pin = lamp_info
    brightness = get_light_to_use(days)

    # Only change if different from last brightness
    if not hasattr(change_light_brightness, "last_brightness"):
        change_light_brightness.last_brightness = 0.0

    if (abs(brightness - change_light_brightness.last_brightness) > 0.01):
        # Only update if >0.01% difference
        rounded_brightness = round(brightness, 2)
        # Convert 0-100% to 0-1000000 microseconds
        duty_cycle = int(rounded_brightness * 10000)

        log(
            f"PWM: Changing brightness from {change_light_brightness.last_brightness:.2f}% to {rounded_brightness:.2f}% (duty={duty_cycle})",
            "DEBUG",
        )

        pi.hardware_PWM(gpio_pin, 1000, duty_cycle)
        change_light_brightness.last_brightness = rounded_brightness

        log(f"PWM: Change completed", "DEBUG")

    current_brightness = brightness
