# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.




# from neopixel import *
#
# # LED strip configuration:
# LED_COUNT      = self._settings.settings.effective['plugins']['monitor']['neopixel_count']      # Number of LED pixels.
# LED_PIN        = self._settings.settings.effective['plugins']['monitor']['neopixel_pin']      # GPIO pin connected to the pixels (must support PWM!).
# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL    = 0
# #LED_STRIP      = ws.SK6812_STRIP_RGBW
# LED_STRIP      = ws.SK6812W_STRIP
#
#
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
# 							  LED_STRIP)
# strip.begin()
def lights_on(strip):
	colorWipe(strip, Color(0, 0, 0, 255))

def lights_off(strip):
	colorWipe(strip, Color(0, 0, 0, 0))

def colorWipe(strip, color):
	"""Wipe color across display a pixel at a time."""
	# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
	# 						  LED_STRIP)
	# Intialize the library (must be called once before other functions).
	# strip.begin()
	color = Color(0, 0, 0, 255)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
