import os
import re
import time
from itertools import chain
from errbot import BotPlugin, re_botcmd
from errbot.core import ErrBot

import config_template
from lib import ApproveHelper, create_sdm_service, PollerHelper, \
    ShowResourcesHelper, ShowRolesHelper, ResourceGrantHelper, RoleGrantHelper, \
    SlackPlatform, MSTeamsPlatform

ACCESS_REGEX = r"\*{0,2}access to (.+)"
APPROVE_REGEX = r"\*{0,2}yes (.+)"
ASSIGN_ROLE_REGEX = r"\*{0,2}access to role (.+)"
SHOW_RESOURCES_REGEX = r"\*{0,2}show available resources\*{0,2}"
SHOW_ROLES_REGEX = r"\*{0,2}show available roles\*{0,2}"
FIVE_SECONDS = 5
ONE_MINUTE = 60

def get_callback_message_fn(bot):
    def callback_message(msg):
        msg.body = bot.plugin_manager.plugins['AccessBot'].clean_up_message(msg.body)
        ErrBot.callback_message(bot, msg)
    return callback_message

def get_platform(bot):
    platform = bot.bot_config.BOT_PLATFORM if hasattr(bot.bot_config, 'BOT_PLATFORM') else None
    if platform == 'ms-teams':
        return MSTeamsPlatform(bot)
    return SlackPlatform(bot)

# pylint: disable=too-many-ancestors
class AccessBot(BotPlugin):
    __grant_requests = {}
    _platform = None

    def activate(self):
        super().activate()
        self._platform = get_platform(self)
        self._bot.MSG_ERROR_OCCURRED = 'An error occurred, please contact your SDM admin'
        self._bot.callback_message = get_callback_message_fn(self._bot)
        self['auto_approve_uses'] = {}
        poller_helper = self.get_poller_helper()
        self.start_poller(FIVE_SECONDS, poller_helper.stale_grant_requests_cleaner)
        self.start_poller(ONE_MINUTE, poller_helper.stale_max_auto_approve_cleaner)
        self._platform.activate()

    def deactivate(self):
        self._platform.deactivate()
        super().deactivate()

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
    def access_resource(self, message, match):
        """
        Grant access to a resource (using the requester's email address)
        """
        resource_name = re.sub(ACCESS_REGEX, "\\1", match.string.replace("*", ""))
        if re.match("^role (.*)", resource_name):
            self.log.debug("##SDM## AccessBot.access better match for assign_role")
            return
        if not self._platform.can_access_resource(message):
            return
        yield from self.get_resource_grant_helper().request_access(message, resource_name)

    @re_botcmd(pattern=ASSIGN_ROLE_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="access to role role-name")
    def assign_role(self, message, match):
        """
        Grant access to all resources in a role (using the requester's email address)
        """
        if not self._platform.can_assign_role(message):
            return
        role_name = re.sub(ASSIGN_ROLE_REGEX, "\\1", match.string.replace("*", ""))
        yield from self.get_role_grant_helper().request_access(message, role_name)

    @re_botcmd(pattern=APPROVE_REGEX, flags=re.IGNORECASE, prefixed=False, hidden=True)
    def approve(self, message, match):
        """
        Approve a grant (resource or role)
        """
        access_request_id = re.sub(APPROVE_REGEX, r"\1", match.string.replace("*", ""))
        approver = message.frm
        yield from self.get_approve_helper().execute(approver, access_request_id)

    #pylint: disable=unused-argument
    @re_botcmd(pattern=SHOW_RESOURCES_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="show available resources")
    def show_resources(self, message, match):
        """
        Show all available resources
        """
        if not self._platform.can_show_resources(message):
            return
        yield from self.get_show_resources_helper().execute()

    #pylint: disable=unused-argument
    @re_botcmd(pattern=SHOW_ROLES_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="show available roles")
    def show_roles(self, message, match):
        """
        Show all available roles
        """
        if not self._platform.can_show_roles(message):
            return
        yield from self.get_show_roles_helper().execute(message)

    @staticmethod
    def get_admins():
        return os.getenv("SDM_ADMINS", "").split(" ")

    @staticmethod
    def get_api_access_key():
        return os.getenv("SDM_API_ACCESS_KEY")

    @staticmethod
    def get_api_secret_key():
        return os.getenv("SDM_API_SECRET_KEY")

    def get_sdm_service(self):
        return create_sdm_service(self.get_api_access_key(), self.get_api_secret_key(), self.log)

    def get_resource_grant_helper(self):
        return ResourceGrantHelper(self)

    def get_role_grant_helper(self):
        return RoleGrantHelper(self)

    def get_approve_helper(self):
        return ApproveHelper(self)

    def get_poller_helper(self):
        return PollerHelper(self)

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self)

    def get_show_roles_helper(self):
        return ShowRolesHelper(self)

    def get_admin_ids(self):
        return self._platform.get_admin_ids()

    def is_valid_grant_request_id(self, request_id):
        return request_id in self.__grant_requests

    def enter_grant_request(self, request_id, message, sdm_object, sdm_account, grant_request_type):
        self.__grant_requests[request_id] = {
            'id': request_id,
            'status': 'PENDING', # TODO Remove?
            'timestamp': time.time(),
            'message': message, # cannot be persisted in errbot state
            'sdm_object': sdm_object,
            'sdm_account': sdm_account,
            'type': grant_request_type
        }

    def remove_grant_request(self, request_id):
        self.__grant_requests.pop(request_id, None)

    def get_grant_request(self, request_id):
        return self.__grant_requests[request_id]

    def get_grant_request_ids(self):
        return list(self.__grant_requests.keys())

    def add_thumbsup_reaction(self, message):
        if self._bot.mode != 'test':
            self._bot.add_reaction(message, "thumbsup")

    def get_sender_nick(self, sender):
        override = self.config['SENDER_NICK_OVERRIDE']
        return override if override else f"@{sender.nick}"
    
    def get_sender_id(self, sender):
        return self._platform.get_sender_id(sender)

    def get_sender_email(self, sender):
        override = self.config['SENDER_EMAIL_OVERRIDE']
        if override:
            return override
        return self._platform.get_sender_email(sender)

    def get_user_nick(self, user):
        return self._platform.get_user_nick(user)

    def increment_auto_approve_use(self, requester_id):
        prev = 0
        if requester_id in self['auto_approve_uses']:
            prev = self['auto_approve_uses'][requester_id]
        with self.mutable('auto_approve_uses') as aau:
            aau[requester_id] = prev + 1
        return self['auto_approve_uses'][requester_id]

    def get_auto_approve_use(self, requester_id):
        if requester_id not in self['auto_approve_uses']:
            return 0
        return self['auto_approve_uses'][requester_id]

    def increase_auto_approve_uses_counter(self):
        prev = 0
        if 'poller_counter' in self['auto_approve_uses']:
            prev = self['auto_approve_uses']['poller_counter']
        with self.mutable('auto_approve_uses') as aau:
            aau['poller_counter'] = prev + ONE_MINUTE # same value used for poller
        return self['auto_approve_uses']['poller_counter']

    def clean_auto_approve_uses(self):
        self['auto_approve_uses'] = {}

    def get_sdm_email_from_profile(self, sender, email_field):
        try:
            user_profile = self._bot.find_user_profile(sender.userid)

            if user_profile['fields'] is None:
                return None

            for field in user_profile['fields'].values():
                if field['label'] == email_field:
                    return field['value']
        except Exception as e:
            self.log.error(
                f"I got an error when trying to get the user profile, you might want to check your account limits."
                f"\n{str(e)}."
            )
        return None

    def clean_up_message(self, message):
        return self._platform.clean_up_message(message)

    def format_access_request_params(self, resource_name, sender_nick, request_id):
        return self._platform.format_access_request_params(resource_name, sender_nick, request_id)

    def format_strikethrough(self, text):
        return self._platform.format_strikethrough(text)

    def add_extra_identifier_args(self, identifier, message):
        return self._platform.add_extra_identifier_args(identifier, message)
