import re
from errbot import BotPlugin, re_botcmd

from lib import AccessHelper, ApproveHelper, HelpHelper, ShowResourcesHelper
import properties

ACCESS_REGEX = r"^access to (.+)$"
APPROVE_REGEX = r"^.{0,2}yes ([a-z0-9]+).{0,2}$"

# pylint: disable=too-many-ancestors
class AccessBot(BotPlugin):
    __access_requests_status = {}

    @re_botcmd(pattern=ACCESS_REGEX, prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        Command which grants access to the named SDM resource.
        """
        resource_name = re.sub(ACCESS_REGEX, "\\1", match.string)
        yield from self.get_access_helper().execute(message, resource_name)

    @re_botcmd(pattern=APPROVE_REGEX, prefixed=False, flags=re.IGNORECASE)
    def approve(self, _, match):
        """
        Command which grants access to the named SDM resource.
        """
        access_request_id = re.sub(APPROVE_REGEX, "\\1", match.string)
        self.get_approve_helper().execute(access_request_id)

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

    def get_access_helper(self):
        return AccessHelper(self)

    def get_approve_helper(self):
        return ApproveHelper(self)

    @staticmethod
    def get_help_helper():
        return HelpHelper()

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self)

    def get_admin_ids(self, admins):
        return [self.build_identifier(admin) for admin in admins]

    def is_access_request_approved(self, access_request_id):
        return self.__access_requests_status[access_request_id] == 'APPROVED'

    def is_valid_access_request_id(self, access_request_id):
        return access_request_id in self.__access_requests_status

    def approve_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'APPROVED'

    def enter_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'PENDING'

    def remove_access_request(self, access_request_id):
        self.__access_requests_status.pop(access_request_id, None)

    def add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
