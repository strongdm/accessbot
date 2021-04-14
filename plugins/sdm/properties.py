import os
import re

class Properties:
    def __init__(
        self, 
        admins,
        admin_timeout,
        api_access_key, 
        api_secret_key,
        sender_override,
        sender_nick,
        sender_email,
        auto_approve_all
    ):
        self.__admins = admins.split(" ")
        self.__admin_timeout = int(admin_timeout)
        self.__api_access_key = api_access_key
        self.__api_secret_key = api_secret_key
        self.__sender_override = True if str(sender_override).lower() == 'true' else False
        self.__sender_nick = sender_nick
        self.__sender_email = sender_email
        self.__auto_approve_all = True if str(auto_approve_all).lower() == 'true' else False

    def admins(self):
        return self.__admins

    def admin_timeout(self):
        return self.__admin_timeout

    def api_access_key(self):
        return self.__api_access_key

    def api_secret_key(self):
        return self.__api_secret_key

    def sender_override(self):
        return self.__sender_override

    def sender_nick(self):
        return self.__sender_nick

    def sender_email(self):
        return self.__sender_email

    def auto_approve_all(self):
        return self.__auto_approve_all


_INSTANCE = Properties(
    os.getenv("SDM_ADMINS", ""),
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
