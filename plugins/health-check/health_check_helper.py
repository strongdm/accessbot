import json
import os
from datetime import datetime

import strongdm


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
        self.sdm_client = strongdm.Client(os.getenv("SDM_API_ACCESS_KEY"), os.getenv("SDM_API_SECRET_KEY"))

    def execute(self):
        health_data = {
            'uptime': self.get_uptime(),
            'plugins_status': self.get_plugins_status(),
            'strongdm_status': self.get_sdm_status()
        }
        return json.dumps(health_data)

    def get_uptime(self):
        return (datetime.now() - self.health_plugin._bot.startup_time).seconds

    def get_plugins_status(self):
        plugins_status = {}
        for status_code, plugin_name in self.health_plugin.status_plugins(None, None)['plugins_statuses']:
            plugins_status[plugin_name] = self.STATUSES[status_code]
        return plugins_status

    def get_sdm_status(self):
        return {
            'resources': self.__get_sdm_entity_status('resources'),
            'roles': self.__get_sdm_entity_status('roles'),
            'accounts': self.__get_sdm_entity_status('accounts'),
            'account_grants': self.__get_sdm_entity_status('account_grants'),
            'account_attachments': self.__get_sdm_entity_status('account_attachments'),
        }

    def __get_sdm_entity_status(self, entity):
        try:
            _ = list(getattr(self.sdm_client, entity).list(''))
        except Exception as e:
            return e.__dict__.get('msg', 'unavailable')
        return 'available'
