def create_config():
    return {
        'ADMIN_TIMEOUT': 2,
        'SENDER_NICK_OVERRIDE': "gbin@localhost",
        'SENDER_EMAIL_OVERRIDE': "gbin@localhost",
        'AUTO_APPROVE_ALL': False,
        'AUTO_APPROVE_TAG': None,
        'HIDE_RESOURCE_TAG': None,
        'GRANT_TIMEOUT': 60,
        'CONTROL_RESOURCES_ROLE_NAME': None,
        'ADMINS_CHANNEL': None,
        'MAX_AUTO_APPROVE_USES': None,
        'MAX_AUTO_APPROVE_INTERVAL': None,
        'USER_ROLES_TAG': 'sdm-roles'
    }

class DummyResource:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class DummyRole:
    def __init__(self, name):
        self.name = name

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
