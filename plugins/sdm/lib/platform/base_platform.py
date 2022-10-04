from abc import ABC, abstractmethod

class BasePlatform(ABC):
    def __init__(self, bot):
        self._bot = bot

    @abstractmethod
    def can_access_resource(self, message):
        pass

    @abstractmethod
    def can_assign_role(self, message):
        pass

    @abstractmethod
    def can_show_resources(self, message):
        pass

    @abstractmethod
    def can_show_roles(self, message):
        pass

    @abstractmethod
    def get_admin_ids(self):
        pass

    @abstractmethod
    def get_sender_id(self, sender):
        pass

    @abstractmethod
    def get_sender_email(self, sender):
        pass

    @abstractmethod
    def get_user_nick(self, approver):
        pass

    @abstractmethod
    def clean_up_message(self, text):
        pass

    @abstractmethod
    def format_access_request_params(self, resource_name, sender_nick):
        pass

    @abstractmethod
    def format_strikethrough(self, text):
        pass

    @abstractmethod
    def format_breakline(self, text):
        pass

    @abstractmethod
    def get_rich_identifier(self, identifier, message):
        pass

    @abstractmethod
    def channel_is_reachable(self, channel):
        pass

    @abstractmethod
    def has_active_admins(self):
        pass

    @abstractmethod
    def use_alternative_emails(self):
        pass

    @abstractmethod
    def channel_match_str_rep(self, channel, str_rep):
        pass

    @abstractmethod
    def format_channel_name(self, channel_name):
        pass

    @abstractmethod
    def get_user_name(self, user):
        pass

    @abstractmethod
    def format_user_handle(self, identifier):
        pass

    @abstractmethod
    def user_is_member_of_channel(self, user, channel):
        pass
