from datetime import datetime
from utils import log
import math

def get_info_for_specific_day(date_to_lookup: str, days: list):
    for day in days:
        if day.get("date") == date_to_lookup:
            return day
    return None

def days_since_summer_solstice(date: datetime)-> int:
    return (date - datetime(date.year,12,21)).days % 365

def light_progress_for_the_day(t: float) -> float:
    # Sun goes up and down. From 0% at sunrise to 100% at midday and back to 0% at sunset
    # This function calculates from 0 to 1 the relative light progress with a sine
    return (1 - math.cos(2 * math.pi * t)) / 2


def absolute_light_for_day_in_year(d: int) -> float:
    # Midday at winter is not the same as midday at summer
    # This function corrects the absolute light emitted adjusting for the day of the year
    # Max is 1 in summer solstice, min is 0.7 in winter solstice
    # intermediate values vary with a sine
    return 0.15 * math.sin(((2 * math.pi * d) / 365) + 1.7524) + 0.85


def get_light_to_use(sunrise_sunset: dict) -> float:
    now = datetime.now()
    log(now.strftime("%Y-%m-%d %H:%M:%S"))
    today = now.strftime("%Y-%m-%d")
    days = sunrise_sunset["results"]

    todays_info = get_info_for_specific_day(today, days)

    if todays_info:
        sunrise = todays_info.get("sunrise")
        sunset = todays_info.get("sunset")
    else:
        print(f"No data was found for {today}, using 9-18")
        sunrise = "9:00:00 AM"
        sunset = "6:00:00 PM"

    sunrise_datetime = datetime.strptime(today + " " + sunrise, "%Y-%m-%d %I:%M:%S %p")
    sunset_datetime = datetime.strptime(today + " " + sunset, "%Y-%m-%d %I:%M:%S %p")

    if sunrise_datetime > now or sunset_datetime < now:
        log("Now is outside of sunrise/sunset range")
        return 0.0

    total_minutes_of_light = (sunset_datetime - sunrise_datetime).total_seconds() / 60

    minutes_of_light_til_now = (now - sunrise_datetime).total_seconds() / 60

    t = minutes_of_light_til_now / total_minutes_of_light
    d = days_since_summer_solstice(now)

    return light_progress_for_the_day(t) * absolute_light_for_day_in_year(d)