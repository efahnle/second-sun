from datetime import datetime
from utils import log
import math


def get_info_for_specific_day(date_to_lookup: str, days: list):
    for day in days:
        if day.get("date") == date_to_lookup:
            return day
    return None


def days_since_summer_solstice(date: datetime) -> int:
    return (date - datetime(date.year, 12, 21)).days % 365


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
    log(now.strftime("%Y-%m-%d %H:%M:%S"), "DEBUG")
    today = now.strftime("%Y-%m-%d")
    days = sunrise_sunset["results"]

    todays_info = get_info_for_specific_day(today, days)

    if todays_info:
        dawn = todays_info.get("dawn")
        dusk = todays_info.get("dusk")
    else:
        print(f"No data was found for {today}, using default dawn/dusk")
        dawn = "6:00:00 AM"
        dusk = "7:00:00 PM"

    dawn_datetime = datetime.strptime(today + " " + dawn, "%Y-%m-%d %I:%M:%S %p")
    dusk_datetime = datetime.strptime(today + " " + dusk, "%Y-%m-%d %I:%M:%S %p")

    if dawn_datetime > now or dusk_datetime < now:
        log("Now is outside of dawn/dusk range", "DEBUG")
        return 0.0

    total_minutes_of_light = (dusk_datetime - dawn_datetime).total_seconds() / 60

    minutes_of_light_til_now = (now - dawn_datetime).total_seconds() / 60

    t = minutes_of_light_til_now / total_minutes_of_light
    d = days_since_summer_solstice(now)

    brightness = light_progress_for_the_day(t) * absolute_light_for_day_in_year(d)

    log(
        f"t: {t}, d: {d}, total_minutes_of_light: {total_minutes_of_light}, minutes_of_light_til_now: {minutes_of_light_til_now}",
        "DEBUG",
    )
    log(f"Brightness: {brightness*100:.2f}%", "DEBUG")

    return brightness * 100
