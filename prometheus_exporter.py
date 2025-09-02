from prometheus_client import Gauge, start_http_server
from light_to_use import (
    light_progress_for_the_day,
    absolute_light_for_day_in_year,
    days_since_summer_solstice,
)
from utils import is_raspberry_pi
from datetime import datetime
import time
import threading

# Define Prometheus metrics
light_is_on = Gauge(
    "second_sun_light_is_on", "Whether the light is currently on (1) or off (0)"
)
light_brightness = Gauge(
    "second_sun_light_brightness", "Current brightness percentage of the light"
)
light_progress_day = Gauge(
    "second_sun_light_progress_day", "Light progress for the current day (0-1)"
)
absolute_light_year = Gauge(
    "second_sun_absolute_light_year",
    "Absolute light value for the current day of year (0.7-1.0)",
)


class PrometheusExporter:
    def __init__(self, port=8000):
        self.port = port
        self.data = None

    def start_server(self):
        """Start the HTTP server for Prometheus metrics"""
        start_http_server(self.port)

    def update_metrics(self, sunrise_sunset_data):
        """Update all Prometheus metrics"""
        self.data = sunrise_sunset_data

        # Get current brightness from shared variable or calculate if not on Pi
        if is_raspberry_pi():
            from hardware import current_brightness

            brightness = current_brightness
        else:
            from light_to_use import get_light_to_use

            brightness = get_light_to_use(sunrise_sunset_data)

        # Update light status and brightness
        light_is_on.set(1 if brightness > 0 else 0)
        light_brightness.set(brightness)

        # Calculate and update light progress for day
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        days = sunrise_sunset_data["results"]

        # Find today's sunrise/sunset
        todays_info = None
        for day in days:
            if day.get("date") == today:
                todays_info = day
                break

        if todays_info:
            sunrise = todays_info.get("sunrise", "9:00:00 AM")
            sunset = todays_info.get("sunset", "6:00:00 PM")

            sunrise_datetime = datetime.strptime(
                today + " " + sunrise, "%Y-%m-%d %I:%M:%S %p"
            )
            sunset_datetime = datetime.strptime(
                today + " " + sunset, "%Y-%m-%d %I:%M:%S %p"
            )

            if sunrise_datetime <= now <= sunset_datetime:
                total_minutes_of_light = (
                    sunset_datetime - sunrise_datetime
                ).total_seconds() / 60
                minutes_of_light_til_now = (now - sunrise_datetime).total_seconds() / 60
                t = minutes_of_light_til_now / total_minutes_of_light
            else:
                t = 0.0
        else:
            t = 0.0

        light_progress_day.set(light_progress_for_the_day(t))

        # Calculate and update absolute light for day in year
        d = days_since_summer_solstice(now)
        absolute_light_year.set(absolute_light_for_day_in_year(d))

    def run_metrics_updater(self):
        """Run metrics updater in a separate thread"""

        def updater():
            while True:
                if self.data:
                    self.update_metrics(self.data)
                time.sleep(30)  # Update metrics every 30 seconds

        thread = threading.Thread(target=updater, daemon=True)
        thread.start()
