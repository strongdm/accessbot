import os

class Properties:
    def __init__(
        self, 
        admin_timeout, 
        admin, 
        sdm_api_access_key, 
        sdm_api_secret_key,
        slack_token,
        slack_sender_override,
        slack_sender_nick,
        slack_sender_email
    ):
        self._admin_timeout = int(admin_timeout)
        self._admin = admin
        self._sdm_api_access_key = sdm_api_access_key
        self._sdm_api_secret_key = sdm_api_secret_key
        self._slack_token = slack_token
        self._slack_sender_override = True if str(slack_sender_override).lower() == 'true' else False
        self._slack_sender_nick = slack_sender_nick
        self._slack_sender_email = slack_sender_email

    def admin_timeout(self):
        return self._admin_timeout

    def admin(self):
        return self._admin

    def sdm_api_access_key(self):
        return self._sdm_api_access_key

    def sdm_api_secret_key(self):
        return self._sdm_api_secret_key

    def slack_token(self):
        return self._slack_token

    def slack_sender_override(self):
        return self._slack_sender_override

    def slack_sender_nick(self):
        return self._slack_sender_nick

    def slack_sender_email(self):
        return self._slack_sender_email


_INSTANCE = Properties(
    os.getenv("SDM_ADMIN_TIMEOUT", "30"),
    os.getenv("SDM_ADMIN"), 
    os.getenv("SDM_API_ACCESS_KEY"),
    os.getenv("SDM_API_SECRET_KEY"),
    os.getenv("SLACK_TOKEN"),
    os.getenv("SLACK_SENDER_OVERRIDE"),
    os.getenv("SLACK_SENDER_NICK"),
    os.getenv("SLACK_SENDER_EMAIL")
) 
def get():
    return _INSTANCE
