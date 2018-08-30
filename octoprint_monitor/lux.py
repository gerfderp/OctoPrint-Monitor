# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BOARD)

def get_lux(pin_to_circuit):
	return time.time()
	count = 0

	# Output on the pin for
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	time.sleep(0.1)

	# Change the pin back to input
	GPIO.setup(pin_to_circuit, GPIO.IN)

	# Count until the pin goes high
	while (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return count


def cleanup():
	GPIO.cleanup()
