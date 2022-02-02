from .slack_platform import SlackPlatform

class SlackBoltPlatform(SlackPlatform):
    def get_sender_email(self, sender):
        email_slack_field = self._bot.config['EMAIL_SLACK_FIELD']
        if email_slack_field:
            sdm_email = self._bot.get_sdm_email_from_profile(sender, email_slack_field)
            if sdm_email:
                return sdm_email
        return sender.email

    def has_active_admins(self):
        for admin_id in self._bot.get_admin_ids():
            if not admin_id.is_deleted:
                return True
        return False
