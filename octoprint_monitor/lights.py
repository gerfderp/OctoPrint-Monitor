# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.


class NeopixelWrapper():
	# LED strip configuration:
	LED_COUNT = 0
	LED_PIN = 0
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0
	strip = ''

	def __init__(self, count, pin):
		self.LED_COUNT = count
		self.LED_PIN = pin
		try:
			from neopixel import *
			self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
									  self.LED_BRIGHTNESS, self.LED_CHANNEL)
			self.strip.begin()

		except ImportError:
			raise ImportError('Neopixel libraries not installed.')

	def lights_on(self):
		self.colorWipe(Color(0, 0, 0, 255))

	def lights_off(self):
		colorWipe(Color(0, 0, 0, 0))

	def colorWipe(color):
		color = Color(0, 0, 0, 255)
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
