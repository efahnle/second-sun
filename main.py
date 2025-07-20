import time
from config import load_config
from hardware import init_gpio

def main():
    config = load_config()
    if config:
        print(f"Configuration loaded successfully: {config}")
        #print(config)
    else:
        print("Failed to load configuration.")
        exit(1)

    light = init_gpio(config.get('gpio_pin', 16))
    print(light)
    while True:
        try:
            for i in range(100,-1,-1):
                light.ChangeDutyCycle(i)
                time.sleep(0.02)           
        
            for i in range(100,-1,-1):
                light.ChangeDutyCycle(100 - i)
                time.sleep(0.02)           
            print("Ciclo completo")
        except KeyboardInterrupt as e:
            light.ChangeDutyCycle(0)
            print("sali")
            light.cleanup()
            raise e



if __name__ == "__main__":
    main()