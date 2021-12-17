from .slack_platform import SlackPlatform

class SlackRTMPlatform(SlackPlatform):
    def get_sender_email(self, sender):
        return sender.email
