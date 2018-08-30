# coding=utf-8
from __future__ import absolute_import
from octoprint.events import eventManager, Events
import octoprint.plugin

# from neopixel import *

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




class MonitorPlugin(octoprint.plugin.SettingsPlugin,
					octoprint.plugin.AssetPlugin,
					octoprint.plugin.TemplatePlugin,
					octoprint.plugin.EventHandlerPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.SimpleApiPlugin,
					octoprint.plugin.ShutdownPlugin):

	light_state = "off"
	lux = 0
	# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
	# 						  LED_STRIP)

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		self._logger.info("Hello World from da Monitor Lizard!")
		self.update_data()
		# strip.begin()

	##~~ ShutdownPlugin mixin
	# def on_shutdown(self):
		# from octoprint_monitor.lux import cleanup
		# cleanup()

	##~~ SimpleAPIPlugin mixin

	def get_api_commands(self):
		return dict(
			lights=[],
			lux=[],
			update=[]
		)

	def on_api_command(self, command, data):
		import flask
		if command == "lights":
			self.light_state = "on" if (self.light_state == "off") else "off"
			# import neopixel
			# neopixel.lights_on(self.strip)
			self._logger.info("lights command called, lights are now {self.light_state}".format(**locals()))
			self.update_data()
			return flask.jsonify(light_state=self.light_state)
		elif command == "lux":
			from octoprint_monitor.lux import get_lux
			self.lux = get_lux(self._settings.settings.effective['plugins']['monitor']['light_pin'])
			self._logger.info("command2 called, lux is {self.lux}".format(**locals()))
			self.update_data()
			return flask.jsonify(lux=self.lux)
		elif command == "update":
			self.update_data()

	def on_api_get(self, request):
		import flask
		return flask.jsonify(foo="bar")

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			neopixel_count="16",
			neopixel_pin="18",
			light_pin="7"

		)

	# ~~ EventHandlerPlugin mixin
	def on_event(self, event, payload):
		if event == Events.CONNECTED:
			self.update_data()

	def update_data(self):
		from octoprint_monitor.lux import get_lux
		self.lux = get_lux(self._settings.settings.effective['plugins']['monitor']['light_pin'])
		data = dict(lux=self.lux, light_state=self.light_state)
		self._plugin_manager.send_plugin_message(self._identifier, data)

	##~~ TemplatePlugin mixin

	def get_template_vars(self):
		return dict(neopixel_count=self._settings.get(["neopixel_count"]),
					light_state=self.light_state,
					lux=self.lux)


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True),
			dict(type="generic", template="monitor.jinja2", custom_bindings=True)
		]

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/monitor.js"],
			css=["css/monitor.css"],
			less=["less/monitor.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			monitor=dict(
				displayName="Monitor Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="gerfderp",
				repo="OctoPrint-Monitor",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/gerfderp/OctoPrint-Monitor/archive/{target_version}.zip"
			)
		)




# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Monitor Plugin"


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = MonitorPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
