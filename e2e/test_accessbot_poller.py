# pylint: disable=invalid-name
import sys
import time
from errbot.backends.base import Message

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
        sender_id = accessbot.build_identifier(config['SENDER_EMAIL_OVERRIDE'])
        accessbot.enter_access_request(Message(frm = sender_id), access_request_id)
        # TODO Uncomment when we start remove time.sleep from access_helper
        # assert access_request_id in accessbot['access_requests']
        accessbot.start_poller(0.5, PollerHelper(accessbot).stale_access_requests_cleaner)

        time.sleep(1)

        # TODO Uncomment when we start remove time.sleep from access_helper
        # assert access_request_id not in accessbot['access_requests']
        assert "timed out" in testbot.pop_message()
        assert "not approved" in testbot.pop_message()

