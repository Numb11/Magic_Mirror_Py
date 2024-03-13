import RPi.GPIO as GPIO
import time
import screen_brightness_control as sc



GPIO.setmode(GPIO.BCM)

TRIGGER_PIN = 10
ECHO_PIN = 20

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def distance(Pulse_Duration):
    return 0.0017 * Pulse_Duration

def Object_Near():
    detected = True
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.0001)
    GPIO.output(TRIGGER_PIN, False)
    return distance(GPIO.input(ECHO_PIN)) < 30

def Set_Use_State():
    CurrentBrightness = sc.get_brightness(display=0)
    if Object_Near() == True:
        sc.set_brightness(20, dislay = 0)
    else:
        sc.set_brightness(90, display = 0)

    


