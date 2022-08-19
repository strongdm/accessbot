import os
import re
from itertools import chain
from errbot import BotPlugin, re_botcmd, Message, webhook
from errbot.core import ErrBot
from slack_sdk.errors import SlackApiError

import config_template
from lib import ApproveHelper, create_sdm_service, MSTeamsPlatform, PollerHelper, \
    ShowResourcesHelper, ShowRolesHelper, SlackBoltPlatform, SlackRTMPlatform, \
    ResourceGrantHelper, RoleGrantHelper, DenyHelper, CommandAliasHelper, ArgumentsHelper, \
    GrantRequestHelper, WhoamiHelper, MetricsHelper, HealthCheckHelper
from lib.util import normalize_utf8
from grant_request_type import GrantRequestType

ACCESS_REGEX = r"access to (.+)"
APPROVE_REGEX = r"yes (\w{4})"
DENY_REGEX = r"no (\w{4}) ?(.+)?"
ASSIGN_ROLE_REGEX = r"access to role (.+)"
SHOW_RESOURCES_REGEX = r"show available resources ?(.+)?"
SHOW_ROLES_REGEX = r"show available roles"
FIVE_SECONDS = 5
ONE_MINUTE = 60
MSG_ERROR_OCCURRED = "An error occurred, please contact your SDM admin"

def get_callback_message_fn(bot):
    def callback_message(msg):
        """
        Executes before the plugin command verification.
        Clears the message removing platform and bold symbols.
        """
        accessbot = bot.plugin_manager.plugins['AccessBot']
        accessbot.check_elevate_admin_user(msg)
        msg.body = accessbot.clean_up_message(msg.body)
        ErrBot.callback_message(bot, msg)
    return callback_message

def get_send_simple_reply(bot):
    def send_simple_reply(msg, text, private=False, threaded=False):
        if text.startswith(MSG_ERROR_OCCURRED):
            accessbot = bot.plugin_manager.plugins['AccessBot']
            accessbot.get_metrics_helper().increment_consecutive_errors()
        return ErrBot.send_simple_reply(bot, msg, text, private=private, threaded=threaded)
    return send_simple_reply

def get_platform(bot):
    platform = bot.bot_config.BOT_PLATFORM if hasattr(bot.bot_config, 'BOT_PLATFORM') else None
    if platform == 'ms-teams':
        return MSTeamsPlatform(bot)
    elif platform == 'slack-classic':
        return SlackRTMPlatform(bot)
    return SlackBoltPlatform(bot)


# pylint: disable=too-many-ancestors
class AccessBot(BotPlugin):
    __grant_requests_helper = None
    __metrics_helper = None
    _platform = None

    def activate(self):
        super().activate()
        self._platform = get_platform(self)
        self._bot.MSG_ERROR_OCCURRED = MSG_ERROR_OCCURRED
        self._bot.callback_message = get_callback_message_fn(self._bot)
        self._bot.send_simple_reply = get_send_simple_reply(self._bot)
        self.init_access_form_bot()
        self.update_access_control_admins()
        self['auto_approve_uses'] = {}
        poller_helper = self.get_poller_helper()
        self.start_poller(FIVE_SECONDS, poller_helper.stale_grant_requests_cleaner)
        self.start_poller(ONE_MINUTE, poller_helper.stale_max_auto_approve_cleaner)
        self.__activate_webserver()

    def __activate_webserver(self):
        webserver = self.get_plugin('Webserver')
        webserver.configure(webserver.get_configuration_template())
        webserver.activate()
        # TODO Extend this check to the rest of the method
        # If something doesn't need to be "instantiated" again we shouldn't be doing it
        if self.__grant_requests_helper is None:
            self.__grant_requests_helper = GrantRequestHelper(self)
        if self.__metrics_helper is None:
            self.__metrics_helper = MetricsHelper(self)
        self._hide_utils_whoami_command()

    def _hide_utils_whoami_command(self):
        # this can change in future versions of errbot
        utils = self.get_plugin('Utils')
        utils.deactivate()
        setattr(utils.whoami.__func__, '_err_command_hidden', True)
        setattr(utils.whoami.__func__, '_err_command_name', 'utils-whoami')
        utils.activate()

    def deactivate(self):
        self.get_plugin('Webserver').deactivate()
        super().deactivate()

    def init_access_form_bot(self):
        if self._bot.bot_config.ACCESS_FORM_BOT_INFO.get('nickname') is not None:
            self._bot.resolve_access_form_bot_id()

    def get_configuration_template(self):
        return config_template.get()

    def configure(self, configuration):
        previous_config = {}
        if hasattr(self, 'config'):
            previous_config = dict(self.config)
        if configuration is not None and configuration != {}:
            admins_channel = configuration.get('ADMINS_CHANNEL')
            if admins_channel is not None and not admins_channel.startswith("#"):
                channel = self._bot.build_identifier(configuration['ADMINS_CHANNEL'])
                configuration['ADMINS_CHANNEL'] = f"#{channel.name}"
            config = dict(chain(config_template.get().items(), configuration.items()))
        elif self._bot.mode != 'test':
            config = config_template.get()
        else:
            config = {}
        super(AccessBot, self).configure(config)
        self.__check_new_bot_state_handling_config(previous_config)

    def __check_new_bot_state_handling_config(self, previous_config):
        if self.__grant_requests_helper is None:
            return
        enable_bot_state_handling = self.config['ENABLE_BOT_STATE_HANDLING']
        if not enable_bot_state_handling and previous_config.get('ENABLE_BOT_STATE_HANDLING'):
            self.__grant_requests_helper.clear_cached_state()
        elif enable_bot_state_handling and not previous_config.get('ENABLE_BOT_STATE_HANDLING'):
            self.__grant_requests_helper.save_state()

    def update_access_control_admins(self):
        self._bot.bot_config.BOT_ADMINS.clear()
        allowed_users = self._bot.bot_config.get_bot_admins()
        self._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms'].clear()
        self._bot.bot_config.ACCESS_CONTROLS['*']['allowprivate'] = True
        self._bot.bot_config.ACCESS_CONTROLS['*']['allowmuc'] = False
        if self.config and self.config['ADMINS_CHANNEL_ELEVATE'] and self.config['ADMINS_CHANNEL']:
            self._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms'].append(self.config['ADMINS_CHANNEL'])
            self._bot.bot_config.ACCESS_CONTROLS['*']['allowprivate'] = False
            self._bot.bot_config.ACCESS_CONTROLS['*']['allowmuc'] = True
            admin_channel = self.build_identifier(self.config['ADMINS_CHANNEL'])
            members = self._bot.conversation_members(admin_channel)
            for member_id in members:
                identifier = self._bot.userid_to_username(member_id)
                allowed_users += [f'@{identifier}']
        self._bot.bot_config.BOT_ADMINS.extend(sorted(set(allowed_users)))

    def check_elevate_admin_user(self, msg):
        if not self.config.get('ADMINS_CHANNEL_ELEVATE') or self.config.get('ADMINS_CHANNEL') is None:
            return
        user_is_admin = f'@{msg.frm.username}' in self._bot.bot_config.BOT_ADMINS
        if hasattr(msg.frm, "room"):
            if f'#{msg.frm.room.channelname}' == self.config['ADMINS_CHANNEL'] and not user_is_admin:
                self._bot.bot_config.BOT_ADMINS.append(f'@{msg.frm.username}')
            return
        if not user_is_admin:
            return
        admins_channel = self.build_identifier(self.config.get('ADMINS_CHANNEL'))
        admins_channel_members = self._bot.conversation_members(admins_channel)
        user_is_member_of_admins_channel = msg.frm.userid in admins_channel_members
        if not user_is_member_of_admins_channel:
            self._bot.bot_config.BOT_ADMINS.remove(f'@{msg.frm.username}')

    def check_configuration(self, configuration):
        pass

    @re_botcmd(pattern=ACCESS_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="access to resource-name [--reason text] [--duration duration]")
    def access_resource(self, message, match):
        """
        Grant access to a resource (using the requester's email address)
        """
        self.__metrics_helper.increment_access_requests()
        arguments = re.sub(ACCESS_REGEX, "\\1", match.string.replace("*", ""), flags=re.IGNORECASE)
        if re.match("^role (.*)", arguments, flags=re.IGNORECASE):
            self.log.debug("##SDM## AccessBot.access better match for assign_role")
            return
        if not self._platform.can_access_resource(message):
            return
        resource_name = self.get_arguments_helper().remove_flags(arguments)
        flags_validators = self.get_resource_grant_helper().get_flags_validators()
        flags = self.get_arguments_helper().extract_flags(arguments, validators=flags_validators)
        try:
            self.get_arguments_helper().check_required_flags(flags_validators.keys(), self.config['REQUIRED_FLAGS'], flags)
            self.check_requester_flag(message, flags.get('requester'))
        except Exception as e:
            yield str(e)
            return
        yield from self.get_resource_grant_helper().request_access(message, resource_name, flags=flags)
        self.__metrics_helper.reset_consecutive_errors()

    @re_botcmd(pattern=ASSIGN_ROLE_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="access to role role-name")
    def assign_role(self, message, match):
        """
        Grant access to all resources in a role (using the requester's email address)
        """
        if not self._platform.can_assign_role(message):
            return
        self.__metrics_helper.increment_access_requests()
        role_name = re.sub(ASSIGN_ROLE_REGEX, "\\1", match.string.replace("*", ""), flags=re.IGNORECASE)
        yield from self.get_role_grant_helper().request_access(message, role_name)
        self.__metrics_helper.reset_consecutive_errors()

    @re_botcmd(pattern=APPROVE_REGEX, flags=re.IGNORECASE, prefixed=False, hidden=True)
    def approve(self, message, match):
        """
        Approve a grant (resource or role)
        """
        self.__metrics_helper.increment_received_messages()
        access_request_id = re.sub(APPROVE_REGEX, r"\1", match.string.replace("*", ""), flags=re.IGNORECASE).upper()
        approver = message.frm
        yield from self.get_approve_helper().execute(approver, access_request_id)
        self.__metrics_helper.reset_consecutive_errors()

    @re_botcmd(pattern=DENY_REGEX, flags=re.IGNORECASE, prefixed=False, hidden=True)
    def deny(self, message, match):
        """
        Deny a grant request (resource or role)
        """
        self.__metrics_helper.increment_received_messages()
        access_request_id = re.sub(DENY_REGEX, r"\1", match.string.replace("*", ""), flags=re.IGNORECASE).upper()
        denial_reason = re.sub(DENY_REGEX, r"\2", match.string.replace("*", ""), flags=re.IGNORECASE)
        admin = message.frm
        yield from self.get_deny_helper().execute(admin, access_request_id, denial_reason)
        self.__metrics_helper.reset_consecutive_errors()

    #pylint: disable=unused-argument
    @re_botcmd(pattern=SHOW_RESOURCES_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="show available resources [--filter expression]")
    def show_resources(self, message, match):
        """
        Show all available resources
        """
        self.__metrics_helper.increment_received_messages()
        if not self._platform.can_show_resources(message):
            return
        flags = self.get_arguments_helper().extract_flags(message.body)
        yield from self.get_show_resources_helper().execute(message, flags=flags)
        self.__metrics_helper.reset_consecutive_errors()

    #pylint: disable=unused-argument
    @re_botcmd(pattern=SHOW_ROLES_REGEX, flags=re.IGNORECASE, prefixed=False, re_cmd_name_help="show available roles")
    def show_roles(self, message, match):
        """
        Show all available roles
        """
        self.__metrics_helper.increment_received_messages()
        if not self._platform.can_show_roles(message):
            return
        yield from self.get_show_roles_helper().execute(message)
        self.__metrics_helper.reset_consecutive_errors()

    @re_botcmd(pattern=r"whoami", flags=re.IGNORECASE, prefixed=False, name="accessbot-whoami")
    def whoami(self, message, _):
        """
        Show your user details
        """
        return self.get_whoami_helper().execute(message)

    @re_botcmd(pattern=r'.+', flags=re.IGNORECASE, prefixed=False, hidden=True)
    def match_alias(self, message, _):
        yield from self.get_command_alias_helper().execute(message)

    @webhook('/health-check')
    def _health_check(self, _):
        return self.get_health_check_helper().execute()

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

    def get_deny_helper(self):
        return DenyHelper(self)

    def get_poller_helper(self):
        return PollerHelper(self)

    def get_show_resources_helper(self):
        return ShowResourcesHelper(self)

    def get_command_alias_helper(self):
        return CommandAliasHelper(self)

    def get_show_roles_helper(self):
        return ShowRolesHelper(self)

    def get_arguments_helper(self):
        return ArgumentsHelper()

    def get_whoami_helper(self):
        return WhoamiHelper(self)

    def get_health_check_helper(self):
        return HealthCheckHelper(self)

    def get_metrics_helper(self):
        return self.__metrics_helper

    def get_admin_ids(self):
        return self._platform.get_admin_ids()

    def enter_grant_request(self, request_id: str, message, sdm_object, sdm_account, grant_request_type: GrantRequestType, flags: dict = None):
        self.__grant_requests_helper.add(request_id, message, sdm_object, sdm_account, grant_request_type, flags)
        self.__metrics_helper.increment_pending_requests()

    def grant_requests_exists(self, request_id: str):
        return self.__grant_requests_helper.exists(request_id)

    def remove_grant_request(self, request_id):
        self.__grant_requests_helper.remove(request_id)
        self.__metrics_helper.decrement_pending_requests()

    def get_grant_request(self, request_id):
        return self.__grant_requests_helper.get(request_id)

    def get_grant_request_ids(self):
        return self.__grant_requests_helper.get_request_ids()

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
        sender_email = self._platform.get_sender_email(sender)
        sdm_email_subaddress = self.config['EMAIL_SUBADDRESS']
        if sdm_email_subaddress:
            return sender_email.replace('@', f'+{sdm_email_subaddress}@')
        return sender_email

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
        except SlackApiError as e:
            if e.response['error'] == 'ratelimited':
                self.log.error(
                    f"Slack throwed a ratelimited error. Too many requests were made\n{str(e)}"
                )
                raise Exception("Too many requests were made. Please, try again in 1 minute") from e
            self.log.error(
                f"I got an error when trying to get the user profile\n{str(e)}"
            )
            raise e
        return None

    def clean_up_message(self, message):
        return self._platform.clean_up_message(normalize_utf8(message))

    def format_access_request_params(self, resource_name, sender_nick):
        return self._platform.format_access_request_params(resource_name, sender_nick)

    def format_strikethrough(self, text):
        return self._platform.format_strikethrough(text)

    def get_rich_identifier(self, identifier, message):
        return self._platform.get_rich_identifier(identifier, message)

    def channel_is_reachable(self, channel):
        return self._platform.channel_is_reachable(channel)

    def has_active_admins(self):
        return self._platform.has_active_admins()

    def check_requester_flag(self, message: Message, requester: str):
        if requester is not None:
            if hasattr(message.frm, "bot_id") and message.frm.bot_id is not None \
                    and message.frm.bot_id == self._bot.bot_config.ACCESS_FORM_BOT_INFO.get('bot_id'):
                previous_channel_id = message.frm.room.id
                message.frm = self.build_identifier(requester)
                message.frm._channelid = previous_channel_id
            else:
                raise Exception("You cannot use the requester flag.")
