import RPi.GPIO as GPIO
import time

pin_led = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_led, GPIO.OUT)


def do_led():
    try:
        GPIO.output(pin_led, True)
        time.sleep(1)
        GPIO.output(pin_led, False)
        time.sleep(1)
    except RuntimeError as ex:
        print("Error prendiendo el led: {}".format(ex))
    finally:
        GPIO.cleanup()
        print("GPIO.cleanup() ejecutado")