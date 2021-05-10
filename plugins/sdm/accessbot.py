import os
import re
import time
from itertools import chain
from errbot import BotPlugin, re_botcmd

import config_template
from lib import AccessHelper, ApproveHelper, ShowResourcesHelper

ACCESS_REGEX = r"^\*{0,2}access to (.+)$"
APPROVE_REGEX = r"^\*{0,2}yes (.+)$"
SHOW_RESOURCES_REGEX = r"^\*{0,2}show available resources\*{0,2}$"

# pylint: disable=too-many-ancestors
class AccessBot(BotPlugin):
    # Intentionally not using errbot persistence
    # See: https://errbot.readthedocs.io/en/latest/user_guide/plugin_development/persistence.html
    # A scheduled clean-up mechanism for stale access requests needs to be implemented first
    __access_requests = {}

    def access_requests_cleaner(self):
        def is_stale(ar_id):
            elapsed_time = (time.time() - self.__access_requests[ar_id]['timestamp']) / 60
            return elapsed_time > self.config['ADMIN_TIMEOUT']
        stale_access_requests = [ar_id for ar_id in self.__access_requests if is_stale(ar_id)]
        for ar_id in stale_access_requests: 
            self.__access_requests.pop(id, None)

    def activate(self):
        super().activate()
        self.start_poller(60, self.access_requests_cleaner)

    def get_configuration_template(self):
        return config_template.get()

    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(config_template.get().items(), configuration.items()))
        else:
            config = config_template.get()
        super(AccessBot, self).configure(config)

    def check_configuration(self, configuration):
        pass

    @re_botcmd(pattern=ACCESS_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="access to resource-name")
    def access(self, message, match):
        """
        Grant access to a resource (using the requester's email address)
        """
        resource_name = re.sub(ACCESS_REGEX, "\\1", match.string.replace("*", ""))
        yield from self.get_access_helper().execute(message, resource_name)

    @re_botcmd(pattern=APPROVE_REGEX, flags=re.IGNORECASE, prefixed=False, hidden=True)
    def approve(self, _, match):
        """
        Approve access to a resource
        """
        access_request_id = re.sub(APPROVE_REGEX, r"\1", match.string.replace("*", ""))
        yield from self.get_approve_helper().execute(access_request_id)

    #pylint: disable=unused-argument
    @re_botcmd(pattern=SHOW_RESOURCES_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="show available resources")
    def show_resources(self, message, match):
        """
        Show all available resources
        """
        yield from self.get_show_resources_helper().execute()

    @staticmethod
    def get_admins():
        return os.getenv("SDM_ADMINS", "").split(" ")
 
    @staticmethod
    def get_api_access_key():
        return os.getenv("SDM_API_ACCESS_KEY")

    @staticmethod
    def get_api_secret_key():
        return os.getenv("SDM_API_SECRET_KEY")

    def get_access_helper(self):
        return AccessHelper(self)

    def get_approve_helper(self):
        return ApproveHelper(self)

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self)

    def get_admin_ids(self):
        return [self.build_identifier(admin) for admin in self.get_admins()]

    def is_access_request_approved(self, access_request_id):
        return self.__access_requests[access_request_id] and \
            self.__access_requests[access_request_id]['status'] == 'APPROVED'

    def is_valid_access_request_id(self, access_request_id):
        return access_request_id in self.__access_requests

    def approve_access_request(self, access_request_id):
        self.__access_requests[access_request_id]['status'] = 'APPROVED'

    def enter_access_request(self, message, access_request_id):
        self.__access_requests[access_request_id] = {
            'status': 'PENDING',
            'timestamp': time.time(),
            'message': message
        }

    def remove_access_request(self, access_request_id):
        self.__access_requests.pop(access_request_id, None)

    def add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
