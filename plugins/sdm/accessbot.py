import re
from errbot import BotPlugin, re_botcmd

from lib import AccessHelper, CallbackMessageHelper, HelpHelper, ShowResourcesHelper
import properties

# pylint: disable=too-many-ancestors
class AccessBot(BotPlugin):
    __access_requests_status = {}

    def callback_message(self, message):
        """
        Callback for handling all messages
        """
        self.get_callback_message_helper().execute(message)
           
    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        Command which grants access to the named SDM resource.
        """
        yield from self.get_access_helper().execute(message, match.string)

    #pylint: disable=unused-argument
    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        Command for showing help
        """
        yield from self.get_help_helper().execute()

    #pylint: disable=unused-argument
    @re_botcmd(pattern=r"^show available resources", prefixed=False, flags=re.IGNORECASE)
    def show_resources(self, message, match):
        """
        Command for showing available resources
        """
        yield from self.get_show_resources_helper().execute()


    @staticmethod
    def get_properties():
        return properties.get()

    def get_callback_message_helper(self):
        return CallbackMessageHelper(self)

    def get_access_helper(self):
        return AccessHelper(self)

    @staticmethod
    def get_help_helper():
        return HelpHelper()

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self)

    def get_admin_ids(self, admins):
        return [self.build_identifier(admin) for admin in admins]

    def is_access_request_granted(self, access_request_id):
        return self.__access_requests_status[access_request_id] == 'APPROVED'

    def grant_access_request(self, access_request_id):
        if not access_request_id in self.__access_requests_status:
            self.log.debug("************** AccessBot.grant_access_request invalid request id = %s", access_request_id)
            return
        self.__access_requests_status[access_request_id] = 'APPROVED'
        self.log.debug("************** AccessBot.grant_access_request approved request id = %s", access_request_id)

    def enter_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'PENDING'

    def remove_access_request(self, access_request_id):
        self.__access_requests_status.pop(access_request_id, None)

    def add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
