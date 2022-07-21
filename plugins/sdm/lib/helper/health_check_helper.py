import json
from datetime import datetime


class HealthCheckHelper:
    # these codes can change in future errbot versions
    STATUSES = {
        'A': 'activated',
        'D': 'deactivated',
        'BA': 'blacklisted',
        'BD': 'blacklisted',
        'C': 'needs to be configured',
    }

    def __init__(self, bot) -> None:
        self.__bot = bot
        self.health_plugin = self.__bot.get_plugin('Health')

    def execute(self):
        health_data = {
            'uptime': self.get_uptime(),
            'plugins_status': self.get_plugins_status()
        }
        return json.dumps(health_data)

    def get_uptime(self):
        return str((datetime.now() - self.health_plugin._bot.startup_time).seconds)

    def get_plugins_status(self):
        plugins_status = {}
        for status_code, plugin_name in self.health_plugin.status_plugins(None, None)['plugins_statuses']:
            plugins_status[plugin_name] = self.STATUSES[status_code]
        return plugins_status
