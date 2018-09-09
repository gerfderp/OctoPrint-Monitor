import RPi.GPIO as GPIO

class NeopixelWrapper():
	# trinket connection configuration:
	LED_PIN = 10

	def __init__(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		print "setting LED_PIN to {pin}".format(**locals())
		self.LED_PIN = pin

	def lights_on(self):
		GPIO.output(self.LED_PIN, GPIO.HIGH)

	def lights_off(self):
		GPIO.output(self.LED_PIN, GPIO.LOW)

	def cleanup(self):
		GPIO.cleanup()
