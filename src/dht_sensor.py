from .utils import log

# Global variables for sensor readings
current_temperature = None
current_humidity = None
_sensor = None
_sensor_enabled = False

def init_dht_sensor(dht_config: dict):
    """Initialize DHT sensor based on configuration"""
    global _sensor, _sensor_enabled
    
    if not dht_config.get("enabled", False):
        log("DHT sensor disabled in configuration", "DEBUG")
        _sensor_enabled = False
        return False
    
    try:
        import board
        import adafruit_dht
        
        sensor_type = dht_config.get("type", "DHT22").upper()
        pin_number = dht_config.get("pin", 4)
        
        # Map pin number to board pin
        pin_map = {
            2: board.D2,
            3: board.D3, 
            4: board.D4,
            17: board.D17,
            27: board.D27,
            22: board.D22
        }
        
        if pin_number not in pin_map:
            log(f"Unsupported DHT sensor pin: {pin_number}")
            return False
            
        board_pin = pin_map[pin_number]
        
        if sensor_type == "DHT22":
            _sensor = adafruit_dht.DHT22(board_pin)
        elif sensor_type == "DHT11":
            _sensor = adafruit_dht.DHT11(board_pin)
        else:
            log(f"Unsupported DHT sensor type: {sensor_type}")
            return False
            
        _sensor_enabled = True
        log(f"DHT sensor ({sensor_type}) initialized on pin {pin_number}", "DEBUG")
        return True
        
    except ImportError as e:
        log(f"DHT sensor libraries not available: {e}. Install with: pip3 install adafruit-circuitpython-dht")
        return False
    except Exception as e:
        log(f"Failed to initialize DHT sensor: {e}")
        return False

def read_sensor_data():
    """Read temperature and humidity from DHT sensor"""
    global current_temperature, current_humidity, _sensor, _sensor_enabled
    
    if not _sensor_enabled or _sensor is None:
        return None, None
    
    try:
        temperature = _sensor.temperature
        humidity = _sensor.humidity
        
        if temperature is not None and humidity is not None:
            current_temperature = temperature
            current_humidity = humidity
            log(f"DHT: {temperature:.1f}°C, {humidity:.1f}%", "DEBUG")
            return temperature, humidity
        else:
            log("DHT sensor returned None values", "DEBUG")
            return None, None
            
    except RuntimeError as error:
        # DHT sensors are prone to read errors, this is normal
        log(f"DHT sensor read error: {error.args[0]}", "DEBUG")
        return None, None
    except Exception as error:
        log(f"DHT sensor error: {error}")
        return None, None

def get_current_readings():
    """Get the last successful sensor readings"""
    return current_temperature, current_humidity

def is_sensor_enabled():
    """Check if DHT sensor is enabled and initialized"""
    return _sensor_enabled

def cleanup_dht_sensor():
    """Clean up DHT sensor resources"""
    global _sensor, _sensor_enabled
    if _sensor and hasattr(_sensor, 'exit'):
        try:
            _sensor.exit()
        except:
            pass
    _sensor = None
    _sensor_enabled = False
    log("DHT sensor cleaned up", "DEBUG")

# Future temperature-based logic framework
def should_disable_light_for_temperature(temperature: float, config: dict) -> bool:
    """
    Future implementation: Check if light should be disabled due to high temperature
    This is a placeholder for temperature-based control logic
    """
    # Get temperature thresholds from config (future feature)
    max_temp = config.get("temperature_limits", {}).get("max_celsius", 35.0)
    
    if temperature is not None and temperature > max_temp:
        log(f"Temperature {temperature:.1f}°C exceeds maximum {max_temp}°C")
        return True
    
    return False

def get_temperature_adjustment_factor(temperature: float, config: dict) -> float:
    """
    Future implementation: Calculate brightness adjustment based on temperature
    Returns multiplier factor (1.0 = no change, <1.0 = reduce brightness)
    """
    # Placeholder for future temperature-based brightness adjustment
    temp_config = config.get("temperature_adjustment", {})
    
    if not temp_config.get("enabled", False) or temperature is None:
        return 1.0
    
    # Example logic: reduce brightness when temperature is high
    reduce_temp = temp_config.get("start_reduce_celsius", 30.0)
    max_temp = temp_config.get("max_celsius", 35.0)
    
    if temperature <= reduce_temp:
        return 1.0
    elif temperature >= max_temp:
        return 0.5  # 50% brightness reduction at max temp
    else:
        # Linear reduction between reduce_temp and max_temp
        factor = 1.0 - (0.5 * (temperature - reduce_temp) / (max_temp - reduce_temp))
        return max(0.5, factor)