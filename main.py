# from hardware import init_gpio, cleanup
from config import load_config
from sunrisesunset import SunriseSunsetWrapper
from utils import log
from apscheduler.schedulers.background import BackgroundScheduler
import time


def display(msg):
    log(msg)


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

    scheduler.add_job(
        display, "interval", seconds=1, args=["every 1 sec"]
    )  # change to 1 min

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
            time.sleep(10)
        except KeyboardInterrupt as e:
            log(f"Shutdown initiated by KeyboardInterrupt. Setting lamp to 0%")
            # light.ChangeDutyCycle(0)
            log("Cleaning up GPIO")
            # cleanup()
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
