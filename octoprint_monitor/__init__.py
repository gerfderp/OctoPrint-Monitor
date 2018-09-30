# coding=utf-8
from __future__ import absolute_import
from octoprint.events import eventManager, Events
import octoprint.plugin


class MonitorPlugin(octoprint.plugin.SettingsPlugin,
					octoprint.plugin.AssetPlugin,
					octoprint.plugin.TemplatePlugin,
					octoprint.plugin.EventHandlerPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.SimpleApiPlugin,
					octoprint.plugin.ShutdownPlugin):

	light_state = "off"
	temp_internal = 0
	temp_external = 0
	humidity = 0
	np = ''
	env = ''
	dht_pin = ''

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		self._logger.info("Hello World from da Monitor Lizard!")
		from octoprint_monitor.lights import NeopixelWrapper
		LED_PIN = int(self._settings.get(["neopixel_pin"]))
		self._logger.info(
			"setting up pixels with PIN of {LED_PIN}.".format(**locals()))
		self.np = NeopixelWrapper(LED_PIN)

		from octoprint_monitor.env import Env
		self.env = Env()

		self.update_data()


	##~~ ShutdownPlugin mixin
	def on_shutdown(self):
		self.np.cleanup()

	##~~ SimpleAPIPlugin mixin

	def get_api_commands(self):
		return dict(
			lights=[],
			update=[]
		)

	def on_api_command(self, command, data):
		import flask
		if command == "lights":
			if (self.light_state == "off"):
				self.light_state = "on"
				self.np.lights_on()
			else:
				self.light_state = "off"
				self.np.lights_off()
			self._logger.info("lights command called, lights are now {self.light_state}".format(**locals()))
			self.update_data()
			return flask.jsonify(light_state=self.light_state)
		elif command == "update":
			self.update_data()

	def on_api_get(self, request):
		import flask
		return flask.jsonify(foo="bar")

	##~~ SettingsPlugin mixin

	# TODO: implement config versions

	def get_settings_defaults(self):
		return dict(
			neopixel_pin="",
			light_pin="",
			dht_pin=""
		)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

	# ~~ EventHandlerPlugin mixin
	def on_event(self, event, payload):
		if event == Events.CONNECTED:
			self.update_data()

	def update_data(self):
		self.env.update(self._settings.get(["dht_pin"]));
		self.temp_internal = self.env.get_temp('internal')

		self.temp_external = self.env.get_temp('external')

		self.humidity = self.env.get_humidity()
		data = dict(light_state=self.light_state,
					temp_internal=self.temp_internal,
					temp_external="{0:.1f}".format(self.temp_external),
					humidity="{0:.1f}".format(self.humidity)
					)
		self._plugin_manager.send_plugin_message(self._identifier, data)

	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
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
