import RPi.GPIO as GPIO
# import fake_rpi.RPi as GPIO
# import time
import sys
# import fake_rpi.Adafruit_DHT
import Adafruit_DHT
from w1thermsensor import W1ThermSensor


class Env():
	humidity = 0
	external = 0
	internal = 0


	def __init__(self):
		pass

	def update(self, pin):
		self.humidity, self.external = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, int(pin))
		for sensor in W1ThermSensor.get_available_sensors():
			self.internal = sensor.get_temperature()

	def get_temp(self, location):
		if location == 'internal':
			return self.internal
		elif location == 'external':
			return self.external

	def get_humidity(self):
		return self.humidity





