import datetime

from grant_request_type import GrantRequestType
from .base_evaluate_request_helper import BaseEvaluateRequestHelper
from ..util import convert_duration_flag_to_timedelta, get_formatted_duration_string


class ApproveHelper(BaseEvaluateRequestHelper):
    def __init__(self, bot):
        super().__init__(bot)
        self.__sdm_service = bot.get_sdm_service()

    def evaluate(self, request_id, **kwargs):
        grant_request = self._bot.get_grant_request(request_id)
        if grant_request['type'] == GrantRequestType.ASSIGN_ROLE:
            yield from self.__approve_assign_role(grant_request)
        else:
            yield from self.__approve_access_resource(grant_request)
        if kwargs.get('is_auto_approve') != None and kwargs['is_auto_approve'] == True:
            yield from self.__register_auto_approve_use(grant_request)

    def __approve_assign_role(self, grant_request):
        yield from self.__grant_temporal_access_by_role(grant_request['sdm_object'].name, grant_request['sdm_account'].id)
        self._bot.add_thumbsup_reaction(grant_request['message'])
        self._bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_assign_role_request_granted(grant_request['message'], grant_request['sdm_object'].name)

    def __approve_access_resource(self, grant_request):
        duration = grant_request['flags'].get('duration')
        self.__grant_temporal_access(grant_request['sdm_object'], grant_request['sdm_account'].id, duration)
        self._bot.add_thumbsup_reaction(grant_request['message'])
        self._bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_access_request_granted(grant_request['message'], grant_request['sdm_object'], duration)

    def __grant_temporal_access_by_role(self, role_name, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self._bot.config['GRANT_TIMEOUT'])
        for resource in self.__sdm_service.get_all_resources_by_role(role_name):
            if self.__sdm_service.account_grant_exists(resource.id, account_id) or self.__sdm_service.role_grant_exists(resource.id, account_id):
                yield f"User already have access to {resource.name}"
                continue
            self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __grant_temporal_access(self, resource, account_id: str, duration: str):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self.__get_resource_grant_timeout(resource, duration=duration))
        self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __notify_access_request_granted(self, message, resource, duration: str):
        sender_email = self._bot.get_sender_email(message.frm)
        sender_nick = self._bot.get_sender_nick(message.frm)
        if duration:
            duration_flag_timedelta = convert_duration_flag_to_timedelta(duration)
            formatted_duration = get_formatted_duration_string(duration_flag_timedelta)
            yield f"{sender_nick}: Granting {sender_email} access to '{resource.name}' for {formatted_duration}"
            return
        grant_timeout = self.__get_resource_grant_timeout(resource)
        yield f"{sender_nick}: Granting {sender_email} access to '{resource.name}' for {grant_timeout} minutes"

    def __notify_assign_role_request_granted(self, message, role_name):
        sender_email = self._bot.get_sender_email(message.frm)
        sender_nick = self._bot.get_sender_nick(message.frm)
        yield f"{sender_nick}: Granting {sender_email} access to resources in role '{role_name}' for {self._bot.config['GRANT_TIMEOUT']} minutes"

    def __register_auto_approve_use(self, grant_request):
        max_auto_approve_uses = self._bot.config['MAX_AUTO_APPROVE_USES']
        if not max_auto_approve_uses:
            return
        requester_id = grant_request['message'].frm.person
        auto_approve_uses = self._bot.increment_auto_approve_use(requester_id)
        yield f"You have {max_auto_approve_uses - auto_approve_uses} remaining auto-approve uses"

    def __get_resource_grant_timeout(self, resource, duration: str = None):
        if duration:
            duration_timedelta = convert_duration_flag_to_timedelta(duration)
            minutes = duration_timedelta.seconds / 60 + duration_timedelta.days * 24 * 60
            return minutes
        grant_timeout_tag = self._bot.config['RESOURCE_GRANT_TIMEOUT_TAG']
        if grant_timeout_tag and resource.tags.get(grant_timeout_tag):
            return int(resource.tags.get(grant_timeout_tag))
        return self._bot.config['GRANT_TIMEOUT']
