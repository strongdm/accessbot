from .slack_platform import SlackPlatform

class SlackRTMPlatform(SlackPlatform):
    def get_sender_email(self, sender):
        return sender.email

    def has_active_admins(self):
        return len(self._bot.get_admins()) > 0
