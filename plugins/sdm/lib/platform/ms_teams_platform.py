import re

from .base_platform import BasePlatform
from ..util import remove_bold_symbols


class MSTeamsPlatform(BasePlatform):
    def can_access_resource(self, message):
        self.__verify_dm_availability(message)
        return True

    def can_assign_role(self, message):
        self.__verify_dm_availability(message)
        return True

    def can_show_resources(self, message):
        self.__verify_dm_availability(message)
        return True

    def can_show_roles(self, message):
        self.__verify_dm_availability(message)
        return True

    def get_admin_ids(self):
        return [self._bot.build_identifier(admin_email) for admin_email in self._bot.get_admins()]

    def get_sender_id(self, sender):
        return sender.email
    
    def get_sender_email(self, sender):
        return sender.email

    def get_user_nick(self, approver):
        return approver.email

    def clean_up_message(self, text):
        unbolded_text = remove_bold_symbols(text.strip())
        return self.clean_message_at_symbols(unbolded_text)

    def clean_message_at_symbols(self, text):
        text_without_bot_mention = self.remove_bot_mention_symbols(text)
        return re.sub(r'<at>|</at>', '', text_without_bot_mention).strip()

    def remove_bot_mention_symbols(self, text):
        return re.sub(r'^<at>[a-zA-Z0-9_ ]+</at>', '', text).strip()

    def format_access_request_params(self, resource_name, sender_nick):
        return f'**{resource_name}**', f'**{sender_nick}**'

    def format_strikethrough(self, text):
        return r"~~" + text + r"~~"

    def format_breakline(self, text):
        return f"{text}<br>"

    def get_rich_identifier(self, identifier, message):
        extras = {
            'team_id': message.extras['conversation'].data['channelData']['team']['id']
        }
        identifier._extras = extras
        return identifier

    def __verify_dm_availability(self, message):
        conversation = message.extras.get('conversation')
        if not conversation or not conversation.data['channelData'].get('team'):
            raise Exception("You cannot execute this command via DM. Please, send a message via a team's channel.")

    def channel_is_reachable(self, channel):
        # TODO: implement logic
        return True

    def has_active_admins(self):
        return len(self._bot.get_admins()) > 0

    def use_alternative_emails(self):
        return self._bot._bot.azure_active_directory_is_configured()

    def channel_match_str_rep(self, channel, str_rep):
        if channel is None:
            return False
        match = re.match(r'(.+)###(.*)', str_rep)
        admin_team_name = match.group(1)
        admin_channel_name = match.group(2)
        return channel.team.name == admin_team_name and \
            (channel.name == admin_channel_name or \
                (channel.name is None and admin_channel_name == ""))

    def format_channel_name(self, channel_name):
        if channel_name is None:
            return None
        match = re.match(r'.+###', channel_name)
        if match is None:
            channel_name += '###'
        return channel_name

    def get_user_name(self, user):
        return user.email

    def format_user_handle(self, identifier):
        return identifier.email

    def user_is_member_of_channel(self, user, channel):
        channel_members = self._bot._bot.conversation_members(channel)
        return user.userid in map(lambda identifier: identifier.userid, channel_members)
