# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BOARD)

def get_temp(location):
	if location == 'internal':
		return 120
	elif location == 'external':
		return 80


def get_humidity():
	return 45


# def cleanup():
	# GPIO.cleanup()
