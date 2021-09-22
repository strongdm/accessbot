import datetime
import shortuuid

from grant_request_type import GrantRequestType

class ApproveHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self, approver, request_id):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug("##SDM## %s ApproveHelper.execute request_id: %s", execution_id, request_id)

        if not self.__bot.is_valid_grant_request_id(request_id):
            self.__bot.log.debug("##SDM## %s ApproveHelper.execute invalid access request id: %s", execution_id, request_id)
            yield f"Invalid access request id = {request_id}"
            return

        if not self.__is_allowed_to_approve(request_id, approver):
            self.__bot.log.debug("##SDM## %s ApproveHelper.execute invalid approver, not an admin to self approve: %s", execution_id, str(approver))
            yield "Invalid approver, not an admin to self approve"
            return

        if not self.__is_admin(approver):
            self.__bot.log.debug("##SDM## %s ApproveHelper.execute invalid approver, not an admin: %s", execution_id, str(approver))
            yield "Invalid approver, not an admin or using the wrong channel"
            return

        self.__bot.log.info("##SDM## %s ApproveHelper.execute approving access to request id: %s", execution_id, request_id)
        yield from self.approve(request_id)

    def approve(self, request_id, is_auto_approve = False):
        grant_request = self.__bot.get_grant_request(request_id)
        if grant_request['type'] == GrantRequestType.ASSIGN_ROLE:
            yield from self.__approve_assign_role(grant_request)
        else:
            yield from self.__approve_access_resource(grant_request)
        if is_auto_approve:
            yield from self.__register_auto_approve_use(grant_request)

    def __is_allowed_to_approve(self, request_id, approver):
        grant_request = self.__bot.get_grant_request(request_id)
        is_self_approve = grant_request['sdm_account'].email == approver.email
        return not is_self_approve or f'@{approver.nick}' in self.__bot.get_admins()

    def __is_admin(self, approver):
        admins_channel = self.__bot.config['ADMINS_CHANNEL']
        approver_channel = None if not hasattr(approver, 'room') else f"#{approver.room.name}"
        if admins_channel:
            return approver_channel == admins_channel
        return self.__bot.get_sender_nick(approver) in self.__bot.get_admins()

    def __approve_assign_role(self, grant_request):
        yield from self.__grant_temporal_access_by_role(grant_request['sdm_object'].name, grant_request['sdm_account'].id)
        self.__bot.add_thumbsup_reaction(grant_request['message'])
        self.__bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_assign_role_request_granted(grant_request['message'], grant_request['sdm_object'].name)

    def __approve_access_resource(self, grant_request):
        self.__grant_temporal_access(grant_request['sdm_object'], grant_request['sdm_account'].id)
        self.__bot.add_thumbsup_reaction(grant_request['message'])
        self.__bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_access_request_granted(grant_request['message'], grant_request['sdm_object'])

    def __grant_temporal_access_by_role(self, role_name, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self.__bot.config['GRANT_TIMEOUT'])
        for resource in self.__sdm_service.get_all_resources_by_role(role_name):
            if self.__sdm_service.account_grant_exists(resource.id, account_id) or self.__sdm_service.role_grant_exists(resource.id, account_id):
                yield f"User already have access to {resource.name}"
                continue
            self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __grant_temporal_access(self, resource, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=self.__get_resource_grant_timeout(resource))
        self.__sdm_service.grant_temporary_access(resource.id, account_id, grant_start_from, grant_valid_until)

    def __notify_access_request_granted(self, message, resource):
        sender_email = self.__bot.get_sender_email(message.frm)
        sender_nick = self.__bot.get_sender_nick(message.frm)
        grant_timeout = self.__get_resource_grant_timeout(resource)
        yield f"{sender_nick}: Granting {sender_email} access to '{resource.name}' for {grant_timeout} minutes"

    def __notify_assign_role_request_granted(self, message, role_name):
        sender_email = self.__bot.get_sender_email(message.frm)
        sender_nick = self.__bot.get_sender_nick(message.frm)
        yield f"{sender_nick}: Granting {sender_email} access to resources in role '{role_name}' for {self.__bot.config['GRANT_TIMEOUT']} minutes"

    def __register_auto_approve_use(self, grant_request):
        max_auto_approve_uses = self.__bot.config['MAX_AUTO_APPROVE_USES']
        if not max_auto_approve_uses:
            return
        requester_id = grant_request['message'].frm.person
        auto_approve_uses = self.__bot.increment_auto_approve_use(requester_id)
        yield f"You have {max_auto_approve_uses - auto_approve_uses} remaining auto-approve uses"

    def __get_resource_grant_timeout(self, resource):
        grant_timeout_tag = self.__bot.config['RESOURCE_GRANT_TIMEOUT_TAG']
        if grant_timeout_tag and resource.tags.get(grant_timeout_tag):
            return int(resource.tags.get(grant_timeout_tag))
        return self.__bot.config['GRANT_TIMEOUT']
