import re

from .base_platform import BasePlatform


class MSTeamsPlatform(BasePlatform):
    def activate(self):
        webserver = self._bot.get_plugin('Webserver')
        webserver.configure(webserver.get_configuration_template())
        webserver.activate()

    def deactivate(self):
        self._bot.get_plugin('Webserver').deactivate()

    def can_access_resource(self, message):
        self.__verify_admins_channel_use()
        self.__verify_dm_availability(message)
        return True

    def can_assign_role(self, message):
        self.__verify_admins_channel_use()
        self.__verify_dm_availability(message)
        return True

    def can_show_resources(self, message):
        self.__verify_dm_availability(message)
        return True

    def can_show_roles(self, message):
        self.__verify_dm_availability(message)
        return True

    def get_admin_ids(self):
        return [self._bot.build_identifier({ 'email': admin_email }) for admin_email in self._bot.get_admins()]

    def get_sender_id(self, sender):
        return sender.email
    
    def get_sender_email(self, sender):
        return sender.email

    def get_user_nick(self, approver):
        return approver.email

    def clean_up_message(self, text):
        unbolded_text = text.replace('*', '')
        return re.sub(r'<at>.+</at>', '', unbolded_text).strip()

    def format_access_request_params(self, resource_name, sender_nick):
        return f'**{resource_name}**', f'**{sender_nick}**'

    def format_strikethrough(self, text):
        return r"~~" + text + r"~~"

    def get_rich_identifier(self, identifier, message):
        extras = {
            'team_id': message.extras['conversation'].data['channelData']['team']['id'],
            'service_url': message.extras['conversation'].data['serviceUrl'],
            'tenant_id': message.extras['conversation'].data['channelData']['tenant']['id']
        }
        identifier._extras = extras
        return identifier

    def __verify_admins_channel_use(self):
        if self._bot.config['ADMINS_CHANNEL']:
            raise Exception("Sorry, it's not possible to request access to resources right now because an \
                Admin Channel was defined, and Microsoft Teams doesn't support Admin's Channels. \
                Please, contact your StrongDM admin.")

    def __verify_dm_availability(self, message):
        conversation = message.extras.get('conversation')
        if not conversation or not conversation.data['channelData'].get('team'):
            raise Exception("You cannot execute this command via DM. Please, send a message via a team's channel.")

    def channel_is_reachable(self, channel):
        return True

    def has_active_admins(self):
        return len(self._bot.get_admins()) > 0
