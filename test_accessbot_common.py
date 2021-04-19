import sys

sys.path.append('plugins/sdm')
from properties import Properties

def create_properties():
    return Properties(
        admins = "gbin@localhost",
        admin_timeout = 2,
        api_access_key = "api-access_key",
        api_secret_key = "c2VjcmV0LWtleQ==",
        sender_nick_override = "testuser",
        sender_email_override = "testuser@localhost",
        auto_approve_all = False,
        auto_approve_tag = None,
        hide_resource_tag = None
    )