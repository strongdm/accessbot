
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
        'ADMINS_CHANNEL': None
    }

class DummyResource:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class DummyRole:
    def __init__(self, name):
        self.name = name
