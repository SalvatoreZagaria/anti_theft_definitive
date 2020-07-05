from pir_sensor import run_pir_sensors, clear_GPIO
from camera import stop_preview

if __name__ == "__main__":
    try:
        run_pir_sensors()
    except KeyboardInterrupt:
        clear_GPIO()
        stop_preview()
