from .base_platform import BasePlatform
from abc import abstractmethod

from ..util import remove_bold_symbols


class SlackPlatform(BasePlatform):
    def can_access_resource(self, message):
        return True

    def can_assign_role(self, message):
        return True

    def can_show_resources(self, message):
        return True

    def can_show_roles(self, message):
        return True

    def get_admin_ids(self):
        return [self._bot.build_identifier(admin) for admin in self._bot.get_admins()]

    def get_sender_id(self, sender):
        return self._bot.get_sender_nick(sender)

    @abstractmethod
    def get_sender_email(self, sender):
        pass

    def get_user_nick(self, approver):
        return f'@{approver.nick}'

    def clean_up_message(self, text):
        return remove_bold_symbols(text)

    def format_access_request_params(self, resource_name, sender_nick):
        return r"\`" + resource_name + r"\`", r"\`" + sender_nick + r"\`"

    def format_strikethrough(self, text):
        return r"~" + text + r"~"

    def format_breakline(self, text):
        return f"{text}\n"

    def get_rich_identifier(self, identifier, message):
        return identifier

    def channel_is_reachable(self, channel_name):
        channel_list = self._bot._bot.channels()
        for channel in channel_list:
            if self.format_channel_name(channel['name']) == self.format_channel_name(channel_name):
                return channel['is_member']
        return False

    def use_alternative_emails(self):
        return False

    def channel_match_str_rep(self, channel, str_rep):
        return channel.__str__() == self.format_channel_name(str_rep)

    def format_channel_name(self, channel_name):
        if channel_name is None:
            return None
        return f'#{channel_name}' if not channel_name.startswith("#") else channel_name

    def get_user_name(self, user):
        username = self._bot._bot.userid_to_username(user)
        return f'@{username}'

    def format_user_handle(self, identifier):
        return f'@{identifier.username}'

    def user_is_member_of_channel(self, user, channel):
        channel_members = self._bot._bot.conversation_members(channel)
        return user.userid in channel_members
