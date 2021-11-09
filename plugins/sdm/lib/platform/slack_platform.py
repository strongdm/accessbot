from .base_platform import BasePlatform


class SlackPlatform(BasePlatform):
    def activate(self):
        pass

    def deactivate(self):
        pass

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

    def get_sender_email(self, sender):
        email_slack_field = self._bot.config['EMAIL_SLACK_FIELD']
        if email_slack_field:
            sdm_email = self._bot.get_sdm_email_from_profile(sender, email_slack_field)
            if sdm_email:
                return sdm_email
        return sender.email

    def get_user_nick(self, approver):
        return f'@{approver.nick}'

    def clean_up_message(self, text):
        return text

    def format_access_request_params(self, resource_name, sender_nick, request_id):
        resource_name = r"\`" + resource_name + r"\`"
        sender_nick = r"\`" + sender_nick + r"\`"
        request_id = r"\`" + request_id + r"\`"
        return resource_name, sender_nick, request_id

    def format_strikethrough(self, text):
        return r"~" + text + r"~"

    def add_extra_identifier_args(self, identifier, message):
        return identifier
