from config import load_config
from sunrisesunset import SunriseSunsetWrapper
from utils import log, is_raspberry_pi
from light_to_use import get_light_to_use
from apscheduler.schedulers.blocking import BlockingScheduler
from prometheus_exporter import PrometheusExporter
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

    # Start Prometheus exporter
    prometheus_port = config.get("prometheus_port", 8000)
    exporter = PrometheusExporter(port=prometheus_port)
    exporter.start_server()
    exporter.data = data
    exporter.run_metrics_updater()
    log(f"Prometheus metrics server started on port {prometheus_port}")

    scheduler = BlockingScheduler()

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
    try:
        scheduler.start()
    except KeyboardInterrupt:
        log(f"Shutdown initiated by KeyboardInterrupt. Setting lamp to 0%")
        if is_raspberry_pi():
            pi, gpio_pin = light
            pi.hardware_PWM(gpio_pin, 1000, 0)  # Turn off light
            log("Cleaning up GPIO")
            cleanup(pi)
        log("Shutting down scheduler")
        scheduler.shutdown(wait=False)
        log("Exit successfully")


"""
    light = init_gpio(config.get("gpio_pin", 16))
    light.ChangeDutyCycle(i)
"""

if __name__ == "__main__":
    main()
