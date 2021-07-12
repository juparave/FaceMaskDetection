import threading
import RPi.GPIO as GPIO
import time

pin_led = 15  # https://pinout.xyz/pinout/pin10_gpio15

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led, GPIO.OUT)


def led_quick(led_event):
    GPIO.output(pin_led, True)
    time.sleep(0.1)
    GPIO.output(pin_led, False)
    time.sleep(0.3)
    GPIO.output(pin_led, True)
    time.sleep(0.1)
    GPIO.output(pin_led, False)
    led_event.clear()


def led(led_event):
    GPIO.output(pin_led, True)
    time.sleep(0.5)
    GPIO.output(pin_led, False)
    time.sleep(0.5)
    led_event.clear()


def do_led(led_event, quick=False):
    if not led_event.isSet():
        led_event.set()
        if quick:
            t1 = threading.Thread(target=led_quick, args=(led_event,))
        else:
            t1 = threading.Thread(target=led, args=(led_event,))
        t1.daemon = True
        t1.start()

    # try:
    #     GPIO.output(pin_led, True)
    #     time.sleep(1)
    #     GPIO.output(pin_led, False)
    #     time.sleep(1)
    # except RuntimeError as ex:
    #     print("Error prendiendo el led: {}".format(ex))
    # finally:
    #     GPIO.cleanup()
    #     print("GPIO.cleanup() ejecutado")
