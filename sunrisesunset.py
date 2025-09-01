import requests
import json
from pathlib import Path
from datetime import date, datetime
from utils import log


class SunriseSunsetWrapper:
    def __init__(self, config: dict):
        self.latitude = config.get("latitude")
        self.longitude = config.get("longitude")
        self.api_url = config.get("api_url", "https://api.sunrisesunset.io/json")
        self.data_file_name = config.get(
            "data_file_name", "data_cache/sunrise_sunset.json"
        )
        # self.gpio_pin = config.get("gpio_pin")

    def get_sunrise_sunset(self) -> dict:
        if self._cache_exists():
            log("Using cached data.")
            return self._get_info_from_from_cache()

        log("Fetching new data from API.")
        data = self._fetch_sunrise_sunset()
        self._save_to_cache(data)
        return data

    def delete_cache_file(self):
        if self._cache_exists():
            Path(self.data_file_name).unlink()
            log(f"Deleted cache file: {self.data_file_name}")
        else:
            log("No cache file to delete.")

    def _fetch_sunrise_sunset(self):
        current_year = datetime.now().year
        first_day_of_year = date(current_year, 1, 1)
        last_day_of_year = date(current_year, 12, 31)

        params = {
            "lat": self.latitude,
            "lng": self.longitude,
            "date_start": first_day_of_year,
            "date_end": last_day_of_year,
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        return response.json()

    def _cache_exists(self) -> bool:
        return Path(self.data_file_name).exists()

    def _get_info_from_from_cache(self) -> dict:
        with open(self.data_file_name, "r") as file:
            return json.load(file)

    def _save_to_cache(self, data: dict):
        Path(self.data_file_name).parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file_name, "w") as file:
            json.dump(data, file, indent=2)
