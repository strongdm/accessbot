from errbot import Message
from errbot.core import ErrBot
from errbot.backends.test import TestPerson as DummyErrbotPerson

from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

admin_default_email = 'gbin@localhost'
bot_admins = [admin_default_email]

class ErrBotExtraTestSettings:
    extra_config = {
        'BOT_ASYNC': False,
        'ACCESS_FORM_BOT_INFO': {},
        'BOT_ADMINS': bot_admins,
        'get_bot_admins': (lambda: [admin_default_email]),
        'ACCESS_CONTROLS': {
            'AccessBot:*': { 'allowusers': ('*') },
            '*': {
                'allowusers': bot_admins,
                'allowrooms': [],
                'allowprivate': True,
                'allowmuc': False,
            }
        },
        'EXPOSE_METRICS': False,
    }
    extra_plugin_dir = "plugins/sdm"


class MSTeamsErrBotExtraTestSettings:
    extra_config = {
        'BOT_ASYNC': False,
        'BOT_PLATFORM': 'ms-teams',
        'ACCESS_FORM_BOT_INFO': {},
        'BOT_ADMINS': bot_admins,
        'get_bot_admins': (lambda: [admin_default_email]),
        'ACCESS_CONTROLS': {
            'AccessBot:*': {'allowusers': ('*')},
            '*': {
                'allowusers': bot_admins,
                'allowrooms': [],
                'allowprivate': True,
                'allowmuc': False,
            }
        },
        'EXPOSE_METRICS': False,
    }
    extra_plugin_dir = "plugins/sdm"


def create_config():
    return {
        'ADMIN_TIMEOUT': 2,
        'SENDER_NICK_OVERRIDE': "gbin@localhost",
        'SENDER_EMAIL_OVERRIDE': "gbin@localhost",
        'AUTO_APPROVE_ALL': False,
        'AUTO_APPROVE_TAG': None,
        'AUTO_APPROVE_ROLE_ALL': False,
        'AUTO_APPROVE_ROLE_TAG': None,
        'AUTO_APPROVE_GROUPS_TAG': None,
        'ALLOW_RESOURCE_TAG': None,
        'HIDE_RESOURCE_TAG': None,
        'CONCEAL_RESOURCE_TAG': None,
        'ALLOW_ROLE_TAG': None,
        'HIDE_ROLE_TAG': None,
        'GRANT_TIMEOUT': 60,
        'CONTROL_RESOURCES_ROLE_NAME': None,
        'ADMINS_CHANNEL': None,
        'ADMINS_CHANNEL_ELEVATE': False,
        'MAX_AUTO_APPROVE_USES': None,
        'MAX_AUTO_APPROVE_INTERVAL': None,
        'USER_ROLES_TAG': None,
        'ENABLE_RESOURCES_FUZZY_MATCHING': True,
        'RESOURCE_GRANT_TIMEOUT_TAG': None,
        'EMAIL_SLACK_FIELD': None,
        'EMAIL_SUBADDRESS': None,
        'GROUPS_TAG': None,
        'REQUIRED_FLAGS': None,
        'APPROVERS_CHANNEL_TAG': None,
        'ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL': False,
        'ENABLE_BOT_STATE_HANDLING': False,
    }


class DummyAccount:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

    def to_dict(self):
        return {
            'name': self.name,
            'tags': self.tags,
        }


class DummyResource:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

    def to_dict(self):
        return {
            'name': self.name,
            'tags': self.tags,
        }


class DummyRole:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags


class DummyConversation:
    def __init__(self, request):
        self._request = request

    @property
    def data(self):
        return self._request

    @property
    def conversation_id(self):
        return self.conversation['id']

    @property
    def activity_id(self):
        return self._request['id']

    @property
    def service_url(self):
        return self._request['serviceUrl']

    @property
    def reply_url(self):
        return '{}/v3/conversations/{}/activities/{}'.format(
            self.service_url,
            self.conversation_id,
            self.activity_id
        )


class DummyPerson(DummyErrbotPerson):
    def __init__(self, person, client=None, nick=None, fullname=None, email=None, is_deleted=False):
        super().__init__(person, client=client, nick=nick, fullname=fullname, email=email)
        self._is_deleted = is_deleted

    @property
    def is_deleted(self):
        return self._is_deleted


class DummyRoom:
    def __init__(self, id, name, is_member=True):
        self.id = id
        self.name = name
        self.is_member = is_member

    @property
    def channelname(self):
        return self.name


class DummyAccountGrant:
    def __init__(self, id):
        self.id = id


# pylint: disable=bad-super-call
def send_message_override(bot, raw_messages):
    # see: https://github.com/errbotio/errbot/blob/master/errbot/backends/test.py#L247
    def sm(msg):
        print(f"\n\n\nMESSAGE:\n{msg.body}\n\n\n")
        # bot.super().send_message(msg)
        super(type(bot), bot).send_message(msg)
        raw_messages.append(msg)
        bot.outgoing_message_queue.put(bot.md.convert(msg.body))

    return sm


def callback_message_fn(bot, from_email=admin_default_email, approver_is_admin=False, from_nick=None, from_username=None,
                        from_userid=None, bot_id=None, room_id=None, room_name=None, check_elevate_admin_user=False):
    def callback_message(msg):
        frm = bot.build_identifier(msg.frm.person)
        frm.bot_id = bot_id
        if from_nick is not None:
            frm._nick = from_nick
        if from_username is not None:
            frm.username = from_username
        if from_userid is not None:
            frm.userid = from_userid
        if room_id is not None or room_name is not None:
            frm.room = DummyRoom(room_id, room_name)
        if approver_is_admin and "yes" in msg.body:
            frm._email = admin_default_email
        else:
            frm._email = from_email
        msg = Message(
            body=msg.body,
            frm=frm,
            to=msg.to,
            parent=msg.parent,
            extras={
                'conversation': DummyConversation({
                    'id': 1,
                    'serviceUrl': 'http://localhost',
                    'channelData': {
                        'team': {
                            'id': 1
                        },
                        'tenant': {
                            'id': 1
                        }
                    }
                })
            }
        )
        if check_elevate_admin_user:
            bot.plugin_manager.plugins['AccessBot'].check_elevate_admin_user(msg)
        ErrBot.callback_message(bot, msg)

    return callback_message


def get_rate_limited_slack_response_error():
    return SlackApiError('ratelimited', SlackResponse(
        data={'ok': False, 'error': 'ratelimited'},
        client=None,
        headers={'retry-after': '0'},
        req_args=None,
        api_url="",
        http_verb="",
        status_code=400
    ))


def get_dummy_person(name, is_deleted=False):
    return DummyPerson(name, is_deleted=is_deleted)
