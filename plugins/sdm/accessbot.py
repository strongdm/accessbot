from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re
import strongdm

from access_helper import AccessHelper
from help_helper import HelpHelper
from access_service import AccessService
import properties 

class AccessBot(BotPlugin):
    access_helper = AccessHelper(properties.get())
    help_helper = HelpHelper()

    def callback_message(self, mess):
        # TODO Make this check case insensitive 
        if mess.body == "yes" and mess.frm == self.build_identifier(properties.get().admin()):
            self.approved = True

    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        A command for showing help
        """
        yield from self.help_helper.execute()

    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """        
        yield from self.access_helper.execute(self, message, match)

