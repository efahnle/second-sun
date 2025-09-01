# Description

`second-sun` is a python program that emulates sunrise and sunset for a PWM-compatible (Pulse width modulation) light for plant growing. The program works with the sunrise and sunset times for a location (latitude and longitude) for each day, increasing and decreasing the brightness of a lamp gradually.

# Tested hardware
- Raspberry Pi 3B+
- 12V 1A generic LED Lamp
- Mosfet and optocoupler module for PWM (YYNMOS-1)

# Requirements
## pigpio for Hardware PWM
This project uses `pigpio` for hardware PWM control, which provides much smoother and more stable PWM output compared to software PWM.

**Installation:**
```bash
sudo apt update
sudo apt install pigpio python3-pigpio
sudo systemctl enable pigpio
sudo systemctl start pigpio
```

**Hardware PWM Pins:**
Only specific GPIO pins support hardware PWM on Raspberry Pi:
- GPIO 12 (Physical pin 32)
- GPIO 13 (Physical pin 33) 
- GPIO 18 (Physical pin 12)
- GPIO 19 (Physical pin 35)

Configure your `gpio_pin` in `config.json` to use one of these pins.

# Prometheus Metrics
The application exposes Prometheus metrics for monitoring and visualization.

**Default port:** 8000 (configurable via `prometheus_port` in `config.json`)

**Available metrics:**
- `second_sun_light_is_on` - Whether the light is currently on (1) or off (0)
- `second_sun_light_brightness` - Current brightness percentage of the light (0-100)
- `second_sun_light_progress_day` - Light progress for the current day (0-1)
- `second_sun_absolute_light_year` - Absolute light value for the current day of year (0.7-1.0)

Access metrics at: `http://raspberry-pi-ip:8000/metrics`

# Sunrise / Sunset API
The project uses the fantastic https://sunrisesunset.io/api/ API to gather the information of the times based on the location. However, to avoid problems with network requests, `second-sun` queries the API once and caches the response in a local JSON file. This file is re-generated once per year. 