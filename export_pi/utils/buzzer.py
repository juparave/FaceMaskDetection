import threading
import time
import RPi.GPIO as GPIO  # Importamos el paquete RPi.GPIO y en el código nos refiriremos a el como GPIO

pin_buzz = 18  # https://pinout.xyz/pinout/pin12_gpio18

GPIO.setmode(GPIO.BCM)  # Establecemos el modo según el cual nos referiremos a los GPIO de nuestra RPi
GPIO.setup(pin_buzz, GPIO.OUT, initial=GPIO.LOW)  # Configuramos el GPIO17 como salida


def buzzer(buzzer_event):
    GPIO.output(pin_buzz, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(pin_buzz, GPIO.LOW)
    buzzer_event.clear()


def do_buzzer(buzzer_event):
    if not buzzer_event.isSet():
        buzzer_event.set()
        t1 = threading.Thread(target=buzzer, args=(buzzer_event,))
        t1.daemon = True
        t1.start()

    # # Contenemos el código principal en una estructura try para limpiar los GPIO al terminar o presentarse un error
    # try:
    #     GPIO.output(pin_buzz, GPIO.HIGH)  # Ponemos en alto el pin del buzzer
    #     time.sleep(1)  # Esperamos un segundo antes de ejecutar la siguiente línea
    #     GPIO.output(pin_buzz, GPIO.LOW)  # Ponemos en alto el pin del buzzer
    #     time.sleep(4)  # Esperamos cuatro segundos antes de ejecutar la siguiente línea
    #
    # except KeyboardInterrupt:
    #     # CTRL+C
    #     print("\nInterrupcion por teclado")
    # except Exception as ex:
    #     print("Error sonando la chicharra: {}".format(ex))
    # finally:
    #     GPIO.cleanup()
    #     print("GPIO.cleanup() ejecutado")
