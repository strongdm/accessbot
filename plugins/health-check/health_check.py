from errbot import BotPlugin, webhook
from health_check_helper import HealthCheckHelper


class HealthCheck(BotPlugin):

    @webhook('/health-check')
    def _health_check(self, _):
        return self.get_health_check_helper().execute()

    def get_health_check_helper(self):
        return HealthCheckHelper(self)
