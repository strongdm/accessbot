# pylint: disable=invalid-name
import sys
import time
from errbot.backends.base import Message
from unittest.mock import MagicMock

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
        accessbot.enter_grant_request(access_request_id, Message(frm = sender_id), MagicMock(), MagicMock(), MagicMock())
        assert access_request_id in accessbot.get_grant_request_ids()
        accessbot.start_poller(0.5, PollerHelper(accessbot).stale_access_requests_cleaner)

        time.sleep(2)

        assert access_request_id not in accessbot.get_grant_request_ids()
        assert "timed out" in testbot.pop_message()
        assert "not approved" in testbot.pop_message()

