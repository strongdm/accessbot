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
        return CallbackMessageHelper(
            log = self.log,
            admin_ids = self.get_admin_ids(self.get_properties().admins()),
            grant_access_request_fn = self.grant_access_request
        )

    def get_access_helper(self):
        return AccessHelper(
            props = self.get_properties(), 
            admin_ids = self.get_admin_ids(self.get_properties().admins()),
            send_fn = self.send,
            is_access_request_granted_fn = self.is_access_request_granted,
            add_thumbsup_reaction_fn = self.add_thumbsup_reaction,
            enter_access_request_fn = self.enter_access_request,
            remove_access_request_fn = self.remove_access_request
        )

    @staticmethod
    def get_help_helper():
        return HelpHelper()

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self.get_properties())

    def get_admin_ids(self, admins):
        return [self.build_identifier(admin) for admin in admins]

    def is_access_request_granted(self, access_request_id):
        return self.__access_requests_status[access_request_id] == 'APPROVED'

    def grant_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'APPROVED'

    def enter_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'PENDING'

    def remove_access_request(self, access_request_id):
        self.__access_requests_status.pop(access_request_id, None)

    def add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
