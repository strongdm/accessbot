import datetime

import strongdm.models
from grant_request_type import GrantRequestType
from .base_evaluate_request_helper import BaseEvaluateRequestHelper
from ..util import convert_duration_flag_to_timedelta, get_formatted_duration_string


class ApproveHelper(BaseEvaluateRequestHelper):
    def __init__(self, bot):
        super().__init__(bot)
        self.__sdm_service = bot.get_sdm_service()

    def evaluate(self, request_id, **kwargs):
        grant_request = self._bot.get_grant_request(request_id)
        if grant_request['type'] == GrantRequestType.ASSIGN_ROLE.value:
            yield from self.__approve_assign_role(grant_request)
        else:
            yield from self.__approve_access_resource(grant_request)
        if kwargs.get('is_auto_approve') != None and kwargs['is_auto_approve'] == True:
            yield from self.__register_auto_approve_use(grant_request)

    def __approve_assign_role(self, grant_request):
        yield from self.__grant_temporal_access_by_role(grant_request['sdm_object'], grant_request['sdm_account'])
        self._bot.add_thumbsup_reaction(grant_request['message'])
        self._bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_assign_role_request_granted(grant_request['message'],
                                                             grant_request['sdm_object'].name,
                                                             grant_request['sdm_account'])
        self._bot.get_metrics_helper().increment_manual_approvals()

    def __approve_access_resource(self, grant_request):
        duration = grant_request['flags'].get('duration')
        resource = grant_request['sdm_object']
        sdm_account = grant_request['sdm_account']
        account_grant_exists = self.__sdm_service.account_grant_exists(resource, sdm_account.id)
        needs_renewal = self._bot.config['ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL'] and account_grant_exists
        if needs_renewal:
            self.__sdm_service.delete_account_grant(resource.id, sdm_account.id)
        self.__grant_temporal_access(grant_request['sdm_object'], grant_request['sdm_account'].id, duration)
        self._bot.add_thumbsup_reaction(grant_request['message'])
        self._bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_access_request_granted(grant_request['message'], resource, duration, needs_renewal)
        self._bot.get_metrics_helper().increment_manual_approvals()

    def __grant_temporal_access_by_role(self, role, account):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self._bot.config['GRANT_TIMEOUT'])
        if isinstance(account, strongdm.models.Service):
            self.__sdm_service.attach_role_to_account(role.id, account.id)
            return
        yield from self.__grant_temporal_access_to_resources_from_role(grant_start_from, grant_valid_until, role.name, account.id)

    def __grant_temporal_access_to_resources_from_role(self, grant_start_from, grant_valid_until, role_name, account_id):
        resources = self.__sdm_service.get_all_resources_by_role(role_name)
        granted_resources_via_account = self.__sdm_service.get_granted_resources_via_account(resources, account_id)
        granted_resources_via_role = self.__sdm_service.get_granted_resources_via_role(resources, account_id)
        granted_resources = self.__remove_duplicated_resources(
            granted_resources_via_account + granted_resources_via_role)
        if len(granted_resources) > 0:
            granted_resources_text = ''
            for resource in granted_resources:
                if granted_resources_text:
                    granted_resources_text += "\n"
                granted_resources_text += f"User already have access to {resource.name}"
            yield granted_resources_text
        # TODO Yield with a specific error when there are no resources to grant
        not_granted_resources = self.__get_not_granted_resources(resources, granted_resources)
        for resource in not_granted_resources:
            self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __grant_temporal_access(self, resource, account_id: str, duration: str):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self.__get_resource_grant_timeout(resource, duration=duration))
        self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __notify_access_request_granted(self, message, resource, duration: str, is_renewal: bool):
        sender_email = self._bot.get_sender_email(message.frm)
        sender_nick = self._bot.get_sender_nick(message.frm)
        if duration:
            duration_flag_timedelta = convert_duration_flag_to_timedelta(duration)
            formatted_duration = get_formatted_duration_string(duration_flag_timedelta)
            yield f"{sender_nick}: Granting {sender_email} access to '{resource.name}' for {formatted_duration}"
            return
        grant_timeout = self.__get_resource_grant_timeout(resource)
        if is_renewal:
            self._notify_requester(message.frm, message, 'Access renewed! The previous grant was revoked and a new one'
                                                          ' was created, you might need to reconnect to the resource.')
        yield f"{sender_nick}: Granting {sender_email} access to '{resource.name}' for {grant_timeout} minutes"

    def __notify_assign_role_request_granted(self, message, role_name, account):
        sender_email = self._bot.get_sender_email(message.frm)
        sender_nick = self._bot.get_sender_nick(message.frm)
        if isinstance(account, strongdm.models.Service):
            # ToDo add timeout info
            yield f"{sender_nick}: Attaching role '{role_name}' to Service Account '{account.name}'"
        else:
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

    def __get_not_granted_resources(self, sdm_resources, granted_resources):
        """
        Removes the intersection about the granted resources and all sdm resources
        """
        granted_resource_ids = [granted_resource.id for granted_resource in granted_resources]
        return [resource for resource in sdm_resources if resource.id not in granted_resource_ids]

    def __remove_duplicated_resources(self, resources):
        mapped_resources_by_id = {}
        for resource in resources:
            if not mapped_resources_by_id.get(resource.id):
                mapped_resources_by_id[resource.id] = resource
        distinct_resources = mapped_resources_by_id.values()
        return distinct_resources
