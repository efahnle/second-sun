from src.config import load_config
from src.sunrisesunset import SunriseSunsetWrapper
from src.utils import log, is_raspberry_pi, set_verbose
from src.light_to_use import get_light_to_use
from apscheduler.schedulers.blocking import BlockingScheduler
from src.prometheus_exporter import PrometheusExporter
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Second Sun - Sunrise/Sunset Light Controller"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    set_verbose(args.verbose)
    config = load_config()
    if config:
        log(f"Configuration loaded successfully: {config}", "DEBUG")
    else:
        log("Failed to load configuration.")
        exit(1)

    sunrise_sunset = SunriseSunsetWrapper(config)
    data = sunrise_sunset.get_sunrise_sunset()
    log(f"Days in response: {len(data['results'])}", "DEBUG")

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
        from src.hardware import init_gpio, cleanup, change_light_brightness
        from src.dht_sensor import init_dht_sensor, read_sensor_data, cleanup_dht_sensor

        light = init_gpio(config.get("gpio_pin", 12))
        scheduler.add_job(
            change_light_brightness, "interval", minutes=1, args=[light, data]
        )
        
        # Initialize DHT sensor if configured
        dht_config = config.get("dht_sensor", {})
        if init_dht_sensor(dht_config):
            log("DHT sensor initialized successfully")
            # Schedule DHT sensor readings every 30 seconds
            scheduler.add_job(read_sensor_data, "interval", seconds=30)
    else:
        log("Not running on Raspberry Pi", "DEBUG")
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
            cleanup_dht_sensor()
        log("Shutting down scheduler")
        scheduler.shutdown(wait=False)
        log("Exit successfully")


if __name__ == "__main__":
    main()
