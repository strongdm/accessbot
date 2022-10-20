import shortuuid
from abc import ABC, abstractmethod
from typing import Any
from ..exceptions import NotFoundException, PermissionDeniedException
from ..util import can_auto_approve_by_tag, fuzzy_match, can_auto_approve_by_groups_tag, get_formatted_duration_string, \
    convert_duration_flag_to_timedelta, get_approvers_channel, AllowedTagEnum, is_hidden, is_allowed, HiddenTagEnum, \
    AllowedGroupsTagEnum
from grant_request_type import GrantRequestType

from metric_type import MetricGaugeType


class BaseGrantHelper(ABC):
    def __init__(self, bot, sdm_service, admin_ids, grant_type, auto_approve_tag_key, auto_approve_all_key):
        self.__bot = bot
        self.__sdm_service = sdm_service
        self.__admin_ids = admin_ids
        self.__grant_type = grant_type
        self.__auto_approve_tag_key = auto_approve_tag_key
        self.__auto_approve_all_key = auto_approve_all_key
        self.__allowed_tag = AllowedTagEnum.RESOURCE if grant_type == GrantRequestType.ACCESS_RESOURCE else AllowedTagEnum.ROLE
        self.__allowed_groups_tag = AllowedGroupsTagEnum.RESOURCE if grant_type == GrantRequestType.ACCESS_RESOURCE else AllowedGroupsTagEnum.ROLE
        self.__hidden_tag = HiddenTagEnum.RESOURCE if grant_type == GrantRequestType.ACCESS_RESOURCE else HiddenTagEnum.ROLE

    def request_access(self, message, searched_name, flags: dict = {}):
        execution_id = shortuuid.ShortUUID().random(length=6)
        operation_desc = self.get_operation_desc()
        self.__bot.log.info("##SDM## %s GrantHelper.access_%s new %s request for entity_name: %s", execution_id, self.__grant_type, operation_desc, searched_name)
        try:
            sdm_resource = self.get_item_by_name(searched_name, execution_id)
            sdm_account = self.__get_account(message)
            self.__check_access_availability(sdm_resource, sdm_account, execution_id)
            self.check_permission(sdm_resource, sdm_account, searched_name)
            request_id = self.generate_grant_request_id()
            yield from self.__grant_access(message, sdm_resource, sdm_account, execution_id, request_id, flags)
        except NotFoundException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s %s request failed %s", execution_id, self.__grant_type, operation_desc, str(ex))
            yield str(ex)
            objects = self.get_all_items()
            if self.can_try_fuzzy_matching():
                yield from self.__try_fuzzy_matching(execution_id, objects, searched_name)
        except PermissionDeniedException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s %s permission denied %s", execution_id, self.__grant_type, operation_desc, str(ex))
            yield str(ex)

    @abstractmethod
    def check_permission(self, sdm_object, sdm_account, searched_name) -> str:
        pass

    @abstractmethod
    def get_all_items(self) -> Any:
        pass

    @abstractmethod
    def get_item_by_name(self, name, execution_id = None) -> Any:
        pass

    @abstractmethod
    def get_operation_desc(self):
        pass

    @abstractmethod
    def can_try_fuzzy_matching(self):
        pass

    def generate_grant_request_id(self):
        request_id = None
        while request_id is None or self.__bot.grant_requests_exists(request_id):
            request_id = shortuuid.ShortUUID().random(length=4).upper()
        return request_id

    def __grant_access(self, message, sdm_object, sdm_account, execution_id, request_id, flags: dict):
        sender_nick = self.__bot.get_sender_nick(message.frm)
        sender_email = sdm_account.email
        self.__bot.log.info("##SDM## %s GrantHelper.__grant_%s sender_nick: %s sender_email: %s", execution_id, self.__grant_type, sender_nick, sender_email)
        if self.__needs_auto_approve(sdm_object, sdm_account) and not self.__reached_max_auto_approve_uses(message.frm.person):
            yield from self.__auto_approve_access_request(message, sdm_object, sdm_account, execution_id, request_id, flags)
            return
        yield from self.__request_manual_approval(message, sdm_object, sdm_account, execution_id, request_id, sender_nick, flags)

    def __enter_grant_request(self, message, sdm_object, sdm_account, grant_request_type, request_id, flags: dict = None):
        self.__bot.enter_grant_request(request_id, message, sdm_object, sdm_account, grant_request_type, flags=flags)

    def __needs_auto_approve(self, sdm_object, sdm_account):
        is_auto_approve_all_enabled = self.__bot.config[self.__auto_approve_all_key]
        return is_auto_approve_all_enabled \
               or can_auto_approve_by_tag(self.__bot.config, sdm_object, self.__auto_approve_tag_key) \
               or can_auto_approve_by_groups_tag(self.__bot.config, sdm_object, sdm_account)

    def __reached_max_auto_approve_uses(self, requester_id):
        max_auto_approve_uses = self.__bot.config['MAX_AUTO_APPROVE_USES']
        if not max_auto_approve_uses:
            return False
        auto_approve_uses = self.__bot.get_auto_approve_use(requester_id)
        return auto_approve_uses >= max_auto_approve_uses

    def __auto_approve_access_request(self, message, sdm_object, sdm_account, execution_id, request_id, flags: dict):
        self.__enter_grant_request(message, sdm_object, sdm_account, self.__grant_type, request_id, flags=flags)
        self.__bot.log.info("##SDM## %s GrantHelper.__grant_%s granting access", execution_id, self.__grant_type)
        yield from self.__bot.get_approve_helper().evaluate(request_id, is_auto_approve=True)
        self.__bot.get_metrics_helper().increment_auto_approvals()

    def __request_manual_approval(self, message, sdm_object, sdm_account, execution_id, request_id, sender_nick, flags: dict):
        approvers_channel_name = get_approvers_channel(self.__bot.config, sdm_object) \
                                 or get_approvers_channel(self.__bot.config, sdm_account)
        self.__check_administration_availability(approvers_channel_name=approvers_channel_name)
        self.__enter_grant_request(message, sdm_object, sdm_account, self.__grant_type, request_id, flags=flags)
        yield from self.__notify_access_request_entered(sender_nick, sdm_object, sdm_account, request_id, message,
                                                        flags, approvers_channel_name=approvers_channel_name)
        self.__bot.log.debug("##SDM## %s GrantHelper.__grant_%s needs manual approval", execution_id, self.__grant_type)

    def __notify_access_request_entered(self, sender_nick, sdm_object, sdm_account, request_id, message, flags: dict,
                                        approvers_channel_name: str = None):
        operation_desc = self.get_operation_desc()
        formatted_resource_name, formatted_sender_nick = self.__bot.format_access_request_params(sdm_object.name, sender_nick)
        if self.__bot.config['ADMINS_CHANNEL'] or approvers_channel_name is not None:
            evaluators_type = 'approvers' if approvers_channel_name is not None else 'admins'
            yield f"Thanks {formatted_sender_nick}, that is a valid request." \
                  f" I'll send a request for approval in the configured {evaluators_type} channel.\n" \
                  f"Your request id is **{request_id}**"
        else:
            team_admins = ", ".join(self.__bot.get_admins())
            yield f"Thanks {formatted_sender_nick}, that is a valid request. Let me check with the team admins: {team_admins}\nYour request id is **{request_id}**"
        duration = convert_duration_flag_to_timedelta(flags.get('duration')) if flags.get('duration') else None
        duration_details = f" for {get_formatted_duration_string(duration)}" if duration else ''
        request_details = f"Hey I have an {operation_desc} request from USER {formatted_sender_nick} for {self.__grant_type.value} {formatted_resource_name}{duration_details}!"
        reason = f" They provided the following reason: \"{flags['reason']}\"." if flags and flags.get('reason') else ''
        approval_instructions = f" To approve, enter: **yes {request_id}**. To deny with a reason, enter: **no {request_id} [optional-reason]**"
        renewal_note = self.__get_renewal_note_message(sdm_object, sdm_account)
        self.__notify_admins(f"{request_details}{reason}{approval_instructions}", message, approvers_channel_name=approvers_channel_name)
        if renewal_note:
            self.__notify_admins(f"{renewal_note}", message, approvers_channel_name=approvers_channel_name)

    def __get_renewal_note_message(self, sdm_object, sdm_account):
        if self.__grant_type is not GrantRequestType.ACCESS_RESOURCE:
            return None
        account_grant_exists = self.__sdm_service.account_grant_exists(sdm_object, sdm_account.id)
        if self.__bot.config['ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL'] and account_grant_exists:
            return "_The user already has access to the resource. Approving the request will revoke the previous " \
                   "grant and create a new one - the user might need to reconnect to the resource._"
        return None

    def __notify_admins(self, text, message, approvers_channel_name: str = None):
        if approvers_channel_name is not None:
            formatted_channel_name = self.__bot.format_channel_name(approvers_channel_name)
            self.__bot.send(self.__bot.build_identifier(formatted_channel_name), text)
            return
        admins_channel = self.__bot.config['ADMINS_CHANNEL']
        if admins_channel:
            self.__bot.send(self.__bot.build_identifier(admins_channel), text)
            return
        for admin_id in self.__admin_ids:
            admin_id = self.__bot.get_rich_identifier(admin_id, message)
            self.__bot.send(admin_id, text)

    def __get_account(self, message):
        return self.__bot.get_sdm_account(message)

    def __try_fuzzy_matching(self, execution_id, term_list, role_name):
        similar_result = fuzzy_match(term_list, role_name)
        if not similar_result:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s there are no similar %ss.", execution_id, self.__grant_type, self.__grant_type)
        else:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s similar role found: %s", execution_id, self.__grant_type, str(similar_result))
            yield f"Did you mean \"{similar_result}\"?"

    def __check_administration_availability(self, approvers_channel_name: str = None):
        if self.__bot.config['APPROVERS_CHANNEL_TAG'] is not None and approvers_channel_name is not None:
            formatted_approvers_channel_name = self.__bot.format_channel_name(approvers_channel_name)
            if not self.__bot.channel_is_reachable(formatted_approvers_channel_name):
                self.__bot.log.error(f"The Channel {formatted_approvers_channel_name} defined as Approver Channel is unreachable."
                                     + f" Probably it's archived or the bot is not in the channel.")
                raise Exception("Sorry, I cannot contact the approvers for this request, their channel is unreachable."
                                + " Please, contact your SDM Admin.")
        elif self.__bot.config['ADMINS_CHANNEL']:
            if not self.__bot.channel_is_reachable(self.__bot.config['ADMINS_CHANNEL']):
                self.__bot.log.error(f"The Channel {self.__bot.config['ADMINS_CHANNEL']} defined as Admin Channel is unreachable."
                                     + f" Probably it's archived or the bot is not in the channel.")
                raise Exception("An Admin Channel was defined but it's unreachable.")
        elif not self.__has_active_admins():
            self.__bot.log.error("There is no active SDM Admin user in Slack Workspace.")
            raise Exception("There is no active Slack Admin to receive your request.")

    def __has_active_admins(self):
        return self.__bot.has_active_admins()

    def __check_access_availability(self, sdm_entity, sdm_account, execution_id):
        if is_hidden(self.__bot.config, self.__hidden_tag, sdm_entity) \
                or not is_allowed(self.__bot.config, self.__allowed_tag, self.__allowed_groups_tag, sdm_entity, sdm_account):
            self.__bot.log.info("##SDM## %s GrantHelper.__get_resource hidden resource", execution_id)
            raise Exception("Access to this resource not available. Please contact your strongDM admins.")
