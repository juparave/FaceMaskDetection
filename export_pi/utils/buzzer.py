import time
import RPi.GPIO as GPIO  # Importamos el paquete RPi.GPIO y en el código nos refiriremos a el como GPIO

pin_buzz = 18  # Variable que contiene el pin(GPIO.BCM) al cual conectamos la señal del LED

GPIO.setmode(GPIO.BOARD)  # Establecemos el modo según el cual nos referiremos a los GPIO de nuestra RPi
GPIO.setup(pin_buzz, GPIO.OUT)  # Configuramos el GPIO18 como salida


def do_buzzer():
    # Contenemos el código principal en una estructura try para limpiar los GPIO al terminar o presentarse un error
    try:
        while 1:  # Implementamos un loop infinito
            GPIO.output(pin_buzz, GPIO.HIGH)  # Ponemos en alto el pin del buzzer
        time.sleep(1)  # Esperamos un segundo antes de ejecutar la siguiente línea
        GPIO.output(pin_buzz, GPIO.LOW)  # Ponemos en alto el pin del buzzer
        time.sleep(4)  # Esperamos cuatro segundos antes de ejecutar la siguiente línea

    except KeyboardInterrupt:
        # CTRL+C
        print("\nInterrupcion por teclado")
    except Exception:
        print("Otra interrupcion")
    finally:
        GPIO.cleanup()
        print("GPIO.cleanup() ejecutado")
