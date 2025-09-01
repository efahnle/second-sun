from config import load_config
from sunrisesunset import SunriseSunsetWrapper
from utils import log, is_raspberry_pi
from light_to_use import get_light_to_use
from apscheduler.schedulers.background import BackgroundScheduler
import time


def main():
    config = load_config()
    if config:
        log(f"Configuration loaded successfully: {config}")
    else:
        log("Failed to load configuration.")
        exit(1)

    sunrise_sunset = SunriseSunsetWrapper(config)
    data = sunrise_sunset.get_sunrise_sunset()
    log(f"Days in response: {len(data['results'])}")

    scheduler = BackgroundScheduler()

    if is_raspberry_pi():
        log("Running on Raspberry Pi")
        from hardware import init_gpio, cleanup, change_light_brightness
        light = init_gpio(config.get("gpio_pin", 16))
        scheduler.add_job(change_light_brightness, "interval", minutes=1, args=[light, data])
    else:
        log("Not running on Raspberry Pi")
        scheduler.add_job(get_light_to_use, "interval", minutes=1, args=[data])

    scheduler.add_job(
        sunrise_sunset.delete_cache_file,
        "cron",
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    scheduler.start()

    while True:
        try:
            time.sleep(60)
            #log("Main loop")
        except KeyboardInterrupt as e:
            log(f"Shutdown initiated by KeyboardInterrupt. Setting lamp to 0%")
            # light.ChangeDutyCycle(0)
            log("Cleaning up GPIO")
            if is_raspberry_pi():
                cleanup()
            log("Shutting down scheduler")
            scheduler.shutdown(wait=False)
            log("Exit successfully")
            raise e


"""
    light = init_gpio(config.get("gpio_pin", 16))
    light.ChangeDutyCycle(i)
"""

if __name__ == "__main__":
    main()
