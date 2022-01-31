import shortuuid
from abc import ABC, abstractmethod
from typing import Any
from ..exceptions import NotFoundException, PermissionDeniedException
from ..util import can_auto_approve_by_tag, fuzzy_match, can_auto_approve_by_groups_tag


class BaseGrantHelper(ABC):
    def __init__(self, bot, sdm_service, admin_ids, grant_type, auto_approve_tag_key, auto_approve_all_key):
        self.__bot = bot
        self.__sdm_service = sdm_service
        self.__admin_ids = admin_ids
        self.__grant_type = grant_type
        self.__auto_approve_tag_key = auto_approve_tag_key
        self.__auto_approve_all_key = auto_approve_all_key

    def request_access(self, message, searched_name):
        execution_id = shortuuid.ShortUUID().random(length=6)
        operation_desc = self.get_operation_desc()
        self.__bot.log.info("##SDM## %s GrantHelper.access_%s new %s request for resource_name: %s", execution_id, self.__grant_type, operation_desc, searched_name)
        try:
            sdm_resource = self.get_item_by_name(searched_name, execution_id)
            sdm_account = self.__get_account(message)
            self.check_permission(sdm_resource, sdm_account, searched_name)
            request_id = self.generate_grant_request_id()
            yield from self.__grant_access(message, sdm_resource, sdm_account, execution_id, request_id)
        except NotFoundException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s %s request failed %s", execution_id, self.__grant_type, operation_desc, str(ex))
            yield str(ex)
            objects = self.get_all_items()
            if self.can_try_fuzzy_matching():
                yield from self.__try_fuzzy_matching(execution_id, objects, searched_name)
        except PermissionDeniedException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s %s permission denied %s", execution_id, self.__grant_type, operation_desc, str(ex))
            yield str(ex)

    # This method needs to be defined on each subclass because of the tests
    # We might come back in the future to try to fix this
    @staticmethod
    @abstractmethod
    def generate_grant_request_id():
        pass

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

    def __grant_access(self, message, sdm_object, sdm_account, execution_id, request_id):
        sender_nick = self.__bot.get_sender_nick(message.frm)
        sender_email = sdm_account.email
        self.__bot.log.info("##SDM## %s GrantHelper.__grant_%s sender_nick: %s sender_email: %s", execution_id, self.__grant_type, sender_nick, sender_email)
        if self.__needs_auto_approve(sdm_object, sdm_account) and not self.__reached_max_auto_approve_uses(message.frm.person):
            yield from self.__auto_approve_access_request(message, sdm_object, sdm_account, execution_id, request_id)
            return
        yield from self.__request_manual_approval(message, sdm_object, sdm_account, execution_id, request_id, sender_nick)

    def __enter_grant_request(self, message, sdm_object, sdm_account, grant_request_type, request_id):
        self.__bot.enter_grant_request(request_id, message, sdm_object, sdm_account, grant_request_type)

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

    def __auto_approve_access_request(self, message, sdm_object, sdm_account, execution_id, request_id):
        self.__enter_grant_request(message, sdm_object, sdm_account, self.__grant_type, request_id)
        self.__bot.log.info("##SDM## %s GrantHelper.__grant_%s granting access", execution_id, self.__grant_type)
        yield from self.__bot.get_approve_helper().approve(request_id, True)

    def __request_manual_approval(self, message, sdm_object, sdm_account, execution_id, request_id, sender_nick):
        self.__check_administration_availability()
        self.__enter_grant_request(message, sdm_object, sdm_account, self.__grant_type, request_id)
        yield from self.__notify_access_request_entered(sender_nick, sdm_object.name, request_id, message)
        self.__bot.log.debug("##SDM## %s GrantHelper.__grant_%s needs manual approval", execution_id, self.__grant_type)

    def __notify_access_request_entered(self, sender_nick, resource_name, request_id, message):
        operation_desc = self.get_operation_desc()
        formatted_resource_name, formatted_sender_nick = self.__bot.format_access_request_params(resource_name, sender_nick)
        if self.__bot.config['ADMINS_CHANNEL']:
            yield f"Thanks {formatted_sender_nick}, that is a valid request. I have created a request for approval in the configured admin channel.\nYour request id is **{request_id}**"
        else:
            team_admins = ", ".join(self.__bot.get_admins())
            yield f"Thanks {formatted_sender_nick}, that is a valid request. Let me check with the team admins: {team_admins}\nYour request id is **{request_id}**"
        self.__notify_admins(f"Hey I have an {operation_desc} request from USER {formatted_sender_nick} for {self.__grant_type.name} {formatted_resource_name}! To approve, enter: **yes {request_id}**", message)

    def __notify_admins(self, text, message):
        admins_channel = self.__bot.config['ADMINS_CHANNEL']
        if admins_channel:
            self.__bot.send(self.__bot.build_identifier(admins_channel), text)
            return
        for admin_id in self.__admin_ids:
            admin_id = self.__bot.get_rich_identifier(admin_id, message)
            self.__bot.send(admin_id, text)

    def __get_account(self, message):
        sender_email = self.__bot.get_sender_email(message.frm)
        return self.__sdm_service.get_account_by_email(sender_email)

    def __try_fuzzy_matching(self, execution_id, term_list, role_name):
        similar_result = fuzzy_match(term_list, role_name)
        if not similar_result:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s there are no similar %ss.", execution_id, self.__grant_type, self.__grant_type)
        else:
            self.__bot.log.error("##SDM## %s GrantHelper.access_%s similar role found: %s", execution_id, self.__grant_type, str(similar_result))
            yield f"Did you mean \"{similar_result}\"?"

    def __check_administration_availability(self):
        if not self.__has_active_admins():
            self.__bot.log.error("There is no active SDM Admin user in Slack Workspace.")
            raise Exception("There is no active Slack Admin to receive your request.")
        if self.__bot.config['ADMINS_CHANNEL'] and not self.__bot.channel_is_reachable(self.__bot.config['ADMINS_CHANNEL']):
            self.__bot.log.error("The Channel defined as Admin Channel is unreachable. Probably it's archived.")
            raise Exception("An Admin Channel was defined but it's unreachable.")

    def __has_active_admins(self):
        return self.__bot.has_active_admins()
