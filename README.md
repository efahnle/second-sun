# Description

`second-sun` is a python program that emulates sunrise and sunset for a PWM-compatible (Pulse width modulation) light for plant growing. The program works with the sunrise and sunset times for a location (latitude and longitude) for each day, increasing and decreasing the brightness of a lamp gradually.

# Tested hardware
- Raspberry Pi 3B+
- 12V 1A generic LED Lamp
- Mosfet and optocoupler module for PWM (YYNMOS-1)

# Sunrise / Sunset API
The project uses the fantastic https://sunrisesunset.io/api/ API to gather the information of the times based on the location. However, to avoid problems with network requests, `second-sun` queries the API once and caches the response in a local JSON file. This file is re-generated once per year. 