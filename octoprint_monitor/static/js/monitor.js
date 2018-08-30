/*
 * View model for OctoPrint-Monitor
 *
 * Author: Gerf Derp
 * License: AGPLv3
 */
$(function() {
    function MonitorViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];
        self.light_state = ko.observable();
        self.lux = ko.observable();

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "monitor") {
				console.log('Ignoring '+plugin);
                return;
            }
            if (data.hasOwnProperty("light_state")) {
                console.log('light_state is now: ' + data.light_state)
                self.light_state = data.light_state;
                $("#light_state").text(self.light_state);
            }
			if(data.hasOwnProperty("lux")) {
				console.log('lux is now: ' + data.lux);
				self.lux = data.lux;
				$("#lux").text(self.lux);
			}
        }
        self.onAfterBinding = function() {
            var control = $('#monitorControl');
            var container = $('#control-jog-general');

            control.insertAfter(container);
            control.css('display', '');
        };
        self.sendLightToggleCommand = function () {
            var pathArray = location.href.split( '/' );
            var protocol = pathArray[0];
            var host = pathArray[2];
            var url = protocol + '//' + host;
            url += '/api/plugin/monitor';
            data = {"command": "lights"};
            console.log('Light Toggle got called. Poking: ' + url + " with data " + data);
            OctoPrint.postJson(url, data, {});
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: MonitorViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "loginStateViewModel", "controlViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_monitor, #tab_plugin_monitor, ...
        elements: [ "#monitorControl" ]
    });
});
