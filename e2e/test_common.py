from errbot import Message
from errbot.core import ErrBot

admin_default_email = 'gbin@localhost'

def create_config():
    return {
        'ADMIN_TIMEOUT': 2,
        'SENDER_NICK_OVERRIDE': "gbin@localhost",
        'SENDER_EMAIL_OVERRIDE': "gbin@localhost",
        'AUTO_APPROVE_ALL': False,
        'AUTO_APPROVE_TAG': None,
        'AUTO_APPROVE_ROLE_ALL': False,
        'AUTO_APPROVE_ROLE_TAG': None,
        'ALLOW_RESOURCE_TAG': None,
        'HIDE_RESOURCE_TAG': None,
        'HIDE_ROLE_TAG': None,
        'GRANT_TIMEOUT': 60,
        'CONTROL_RESOURCES_ROLE_NAME': None,
        'ADMINS_CHANNEL': None,
        'MAX_AUTO_APPROVE_USES': None,
        'MAX_AUTO_APPROVE_INTERVAL': None,
        'USER_ROLES_TAG': None,
        'ENABLE_RESOURCES_FUZZY_MATCHING': True,
        'RESOURCE_GRANT_TIMEOUT_TAG': None,
        'EMAIL_SLACK_FIELD': None
    }

class DummyAccount:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class DummyResource:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

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

def callback_message_fn(bot, from_email=admin_default_email, approver_is_admin=False):
    def callback_message(msg):
        frm = msg.frm
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
        ErrBot.callback_message(bot, msg)
    return callback_message
