from plugins.sdm.lib.improver.improver import BaseImprover


class SlackImprover(BaseImprover):

    def get_admin_ids(self):
        return [self._bot.build_identifier(admin) for admin in self._bot.get_admins()]

    def get_sender_id(self, sender):
        return self._bot.get_sender_nick(sender)

    def get_sender_email(self, sender):
        email_slack_field = self._bot.config['EMAIL_SLACK_FIELD']
        if email_slack_field:
            sdm_email = self._bot.__get_sdm_email_from_profile(sender, email_slack_field)
            if sdm_email:
                return sdm_email
        return super().get_sender_email(sender)

    def clean_up_message(self, text):
        return text

    def format_access_request_params(self, resource_name, sender_nick, request_id):
        resource_name = r"\'" + resource_name + r"\'"
        sender_nick = r"\'" + sender_nick + r"\'"
        request_id = r"\'" + request_id + r"\'"
        return resource_name, sender_nick, request_id

    def format_strikethrough(self, text):
        return r"~" + text + r"~"
