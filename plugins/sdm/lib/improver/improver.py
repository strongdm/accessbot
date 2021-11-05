import re
from abc import ABC, abstractmethod


class BaseImprover(ABC):

    def __init__(self, bot):
        self._bot = bot

    def activate(self):
        pass

    def deactivate(self):
        pass

    def can_access_resource(self, resource_name, message):
        if re.match("^role (.*)", resource_name):
            self._bot.log.debug("##SDM## AccessBot.access better match for assign_role")
            return False
        return True

    def can_assign_role(self, message):
        return True

    def can_show_resources(self, message):
        return True

    def can_show_roles(self, message):
        return True

    @abstractmethod
    def get_admin_ids(self):
        pass

    @abstractmethod
    def get_sender_id(self, sender):
        pass

    def get_sender_email(self, sender):
        return sender.email

    def get_user_nick(self, approver):
        return f'@{approver.nick}'

    @abstractmethod
    def clean_up_message(self, text):
        pass

    @abstractmethod
    def format_access_request_params(self, resource_name, sender_nick, request_id):
        pass

    @abstractmethod
    def format_strikethrough(self, text):
        pass
