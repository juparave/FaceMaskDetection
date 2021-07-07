import RPi.GPIO as GPIO
import time

pin_led = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_led, GPIO.OUT)


def do_led():
    try:
        GPIO.output(7, True)
        time.sleep(1)
        GPIO.output(7, False)
        time.sleep(1)
    except RuntimeError as ex:
        print("Error prendiendo el led: {}".format(ex))
    finally:
        GPIO.cleanup()
        print("GPIO.cleanup() ejecutado")