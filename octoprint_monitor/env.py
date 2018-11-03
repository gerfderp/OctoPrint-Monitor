try:
	import Adafruit_DHT
	from w1thermsensor import W1ThermSensor
except ImportError:
	from fake_rpi import Adafruit_DHT
	from fake_rpi import W1ThermSensor

class Env():

	def __init__(self, pin):
		self.dht_pin = int(pin)
		self.humidity = 0
		self.external = 0
		self.internal = 0

	def update(self):
		self.humidity, self.external = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.dht_pin)
		for sensor in W1ThermSensor.get_available_sensors():
			self.internal = sensor.get_temperature()

	def get_temp(self, location):
		if location == 'internal':
			return self.internal
		elif location == 'external':
			return self.external

	def get_humidity(self):
		return self.humidity





