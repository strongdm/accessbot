from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re
import strongdm

from lib import access_helper, callback_message_helper, help_helper
import properties 

class AccessBot(BotPlugin):
    access_requests_status = {}

    def callback_message(self, message):
        """
        A callback for handling all messages
        """
        admin_id = self.build_identifier(properties.get().admin())
        yield from self.get_callback_message_helper().execute(self, admin_id, message)

    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        A command for showing help
        """
        yield from self.get_help_helper().execute()

    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """        
        yield from self.get_access_helper().execute(self, message, match)

    def get_access_helper(self):
        return access_helper

    def get_help_helper(self):
        return help_helper
