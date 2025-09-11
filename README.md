# Description

`second-sun` is a Python program that emulates natural lighting cycles for plant growing using PWM-controlled LED lights. The program uses **dawn and dusk times** (not just sunrise/sunset) for extended daily light exposure, gradually adjusting brightness throughout the day based on your geographic location.

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

# Running as a System Service

To run Second Sun automatically on boot as a systemd service:

**Installation:**
```bash
# Install dependencies
sudo pip3 install -r requirements.txt

# Copy service file to systemd directory
sudo cp examples/second-sun.service /etc/systemd/system/

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable second-sun.service

# Start the service
sudo systemctl start second-sun.service

# Check service status
sudo systemctl status second-sun.service

# View logs
sudo journalctl -u second-sun.service -f
```

**Command Line Options:**
- `python3 main.py` - Run with minimal logging (production)
- `python3 main.py -v` or `--verbose` - Run with detailed debug logging

# Prometheus Metrics
The application exposes Prometheus metrics for monitoring and visualization.

**Default port:** 8000 (configurable via `prometheus_port` in `config.json`)

**Available metrics:**
- `second_sun_light_is_on` - Whether the light is currently on (1) or off (0)
- `second_sun_light_brightness` - Current brightness percentage of the light (0-100)
- `second_sun_light_progress_day` - Light progress for the current day (0-1)
- `second_sun_absolute_light_year` - Absolute light value for the current day of year (0.7-1.0)

Access metrics at: `http://raspberry-pi-ip:8000/metrics`

# Docker Compose Setup (Optional)
For monitoring setup with Prometheus and Grafana, sample configuration files are provided in the `examples/` directory:

- `examples/compose.yaml` - Docker Compose setup for Prometheus + Grafana
- `examples/prometheus/prometheus.yaml` - Prometheus configuration
- `examples/grafana/grafana.yaml` - Grafana datasource configuration  
- `examples/grafana/grafana-dashboard.json` - Pre-built dashboard for Second Sun metrics

**Quick start:**
```bash
cd examples/
docker compose up -d
# Grafana: http://localhost:3000 (credentials are in the compose file)
# Prometheus: http://localhost:9090
```

# Sample Grafana dashboard

<img width="1563" height="873" alt="image" src="https://github.com/user-attachments/assets/84d37cca-2e51-41ef-b94b-af4bffd2bf42" />

# Configuration
Configuration is managed through `config.json`:

```json
{
  "latitude": -34.60368,
  "longitude": -58.38156, 
  "api_url": "https://api.sunrisesunset.io/json",
  "data_file_name": "data/data_cache/sunrise_sunset.json",
  "gpio_pin": 12,
  "prometheus_port": 8000
}
```

# Features
- **Dawn-to-dusk lighting**: Uses dawn and dusk times for maximum daily light exposure (~30 minutes longer than sunrise/sunset)
- **Smooth brightness curves**: Natural sine-wave progression mimicking real sunlight intensity
- **Seasonal adjustment**: Light intensity varies based on time of year (summer brighter than winter)
- **Hardware PWM**: Jitter-free lighting using Raspberry Pi's dedicated PWM hardware. Avoid software PWM!
- **Automatic caching**: API data cached locally, refreshed annually
- **Production ready**: Systemd service integration with proper logging levels
- **Monitoring**: Prometheus metrics with pre-built Grafana dashboard
- **Offline capable**: Works without internet after initial API fetch

# API Data Source
The project uses the fantastic https://sunrisesunset.io/api/ API to gather the information of the times based on the location. However, to avoid problems with network requests, `second-sun` queries the API once and caches the response in a local JSON file. This file is re-generated once per year. 
