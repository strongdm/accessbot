# pylint: disable=invalid-name
import sys
import time

from test_common import create_config
sys.path.append('plugins/sdm')
from lib import PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

access_request_id = "12ab"

class Test_stale_access_requests_cleaner:
    def test_poller(self, testbot):
        config = create_config()
        config['ADMIN_TIMEOUT'] = 0

        accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config = config
        accessbot.enter_access_request({}, access_request_id)
        assert access_request_id in accessbot['access_requests']
        accessbot.start_poller(1, PollerHelper(accessbot).stale_access_requests_cleaner)

        time.sleep(2)
        assert access_request_id not in accessbot['access_requests']
