from errbot import Message
import sys
from unittest.mock import MagicMock, patch, mock_open

sys.path.append('e2e/')
sys.path.append('plugins/sdm/')

from test_common import DummyResource, DummyAccount, DummyPerson, DummyConversation
from .grant_request_helper import GrantRequestHelper
from grant_request_type import GrantRequestType

request_id = "12AB"
resource_name = "xxx"
account_name = "xxx"
mock_file_data = '[{"id": "12AB", "timestamp": 1653069610.2132611, "message": {"frm": "gbin@localhost", "to": "gbin@localhost", "extras": {}}, "sdm_object": {"name": "xxx", "tags": {}}, "sdm_account": {"name": "xxx", "tags": {}}, "type": 0, "flags": null}]'


class Test_state_handling:
    def test_save_state_when_has_pending_requests(self):
        bot = get_mock_bot()
        helper = GrantRequestHelper(bot)
        with patch("builtins.open", mock_open()) as handle:
            helper.add(request_id, get_mock_message(), get_mock_sdm_object(), get_mock_sdm_account(), GrantRequestType.ACCESS_RESOURCE)
            assert helper.get(request_id) is not None
            assert helper.exists(request_id)
            assert len(helper.get_request_ids()) == 1
            file = handle()
            file.write.assert_called_once()
            helper.remove(request_id)
            assert helper.get(request_id) is None
            assert not helper.exists(request_id)

    def test_restore_state_when_has_stored_requests(self):
        bot = get_mock_bot()
        with patch("builtins.open", mock_open(read_data=mock_file_data)) as handle:
            helper = GrantRequestHelper(bot)
            assert helper.get(request_id) is not None
            assert helper.exists(request_id)
            assert len(helper.get_request_ids()) == 1
            file = handle()
            file.read.assert_called_once()
            helper.remove(request_id)
            assert helper.get(request_id) is None
            assert not helper.exists(request_id)


def get_mock_bot():
    mock = MagicMock()
    mock.mode = ""
    return mock

def get_mock_message():
    mock = Message(
        body="",
        frm=DummyPerson("gbin@localhost"),
        to=DummyPerson("gbin@localhost"),
        parent=None,
        extras={}
    )
    return mock

def get_mock_sdm_object():
    return DummyResource(resource_name, {})

def get_mock_sdm_account():
    return DummyAccount(resource_name, {})
