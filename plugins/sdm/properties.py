import os

class Properties:
    def __init__(
        self, 
        admin,
        admin_timeout,
        api_access_key, 
        api_secret_key,
        sender_override,
        sender_nick,
        sender_email,
        auto_approve_all
    ):
        self._admin = admin
        self._admin_timeout = int(admin_timeout)
        self._api_access_key = api_access_key
        self._api_secret_key = api_secret_key
        self._sender_override = True if str(sender_override).lower() == 'true' else False
        self._sender_nick = sender_nick
        self._sender_email = sender_email
        self._auto_approve_all = True if str(auto_approve_all).lower() == 'true' else False

    def admin(self):
        return self._admin

    def admin_timeout(self):
        return self._admin_timeout

    def api_access_key(self):
        return self._api_access_key

    def api_secret_key(self):
        return self._api_secret_key

    def sender_override(self):
        return self._sender_override

    def sender_nick(self):
        return self._sender_nick

    def sender_email(self):
        return self._sender_email

    def auto_approve_all(self):
        return self._auto_approve_all


_INSTANCE = Properties(
    os.getenv("SDM_ADMIN"),
    os.getenv("SDM_ADMIN_TIMEOUT", "30"),
    os.getenv("SDM_API_ACCESS_KEY"),
    os.getenv("SDM_API_SECRET_KEY"),
    os.getenv("SDM_SENDER_OVERRIDE", ""),
    os.getenv("SDM_SENDER_NICK"),
    os.getenv("SDM_SENDER_EMAIL"),
    os.getenv("SDM_AUTO_APPROVE_ALL")
) 
def get():
    return _INSTANCE
