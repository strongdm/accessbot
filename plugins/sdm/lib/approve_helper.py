import datetime
import shortuuid

from grant_request_type import GrantRequestType

class ApproveHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self, request_id):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug("##SDM## %s ApproveHelper.execute request_id: %s", execution_id, request_id)

        if not self.__bot.is_valid_grant_request_id(request_id):
            self.__bot.log.debug("##SDM## %s ApproveHelper.execute invalid access request id: %s", execution_id, request_id)
            yield f"Invalid access request id = {request_id}"
            return

        self.__bot.log.info("##SDM## %s ApproveHelper.execute approving access to request id: %s", execution_id, request_id)
        yield from self.approve(request_id)

    def approve(self, request_id):
        grant_request = self.__bot.get_grant_request(request_id)
        if grant_request['type'] == GrantRequestType.ASSIGN_ROLE:
            yield from self.__approve_assign_role(grant_request)
            return
        yield from self.__approve_access_resource(grant_request)

    def __approve_assign_role(self, grant_request):
        self.__grant_temporal_access_by_role(grant_request['sdm_object'].name, grant_request['sdm_account'].id)
        self.__bot.add_thumbsup_reaction(grant_request['message'])
        self.__bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_assign_role_request_granted(grant_request['message'], grant_request['sdm_object'].name)

    def __approve_access_resource(self, grant_request):
        self.__grant_temporal_access(grant_request['sdm_object'].id, grant_request['sdm_account'].id)
        self.__bot.add_thumbsup_reaction(grant_request['message'])
        self.__bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_access_request_granted(grant_request['message'], grant_request['sdm_object'].name)

    def __grant_temporal_access_by_role(self, role_name, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes = self.__bot.config['GRANT_TIMEOUT'])
        self.__sdm_service.grant_temporary_access_by_role(role_name, account_id, grant_start_from, grant_valid_until)

    def __grant_temporal_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes = self.__bot.config['GRANT_TIMEOUT'])
        self.__sdm_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)

    def __notify_access_request_granted(self, message, resource_name):
        sender_email = self.__bot.get_sender_email(message)
        sender_nick = self.__bot.get_sender_nick(message)
        yield f"@{sender_nick}: Granting {sender_email} access to '{resource_name}' for {self.__bot.config['GRANT_TIMEOUT']} minutes"

    def __notify_assign_role_request_granted(self, message, role_name):
        sender_email = self.__bot.get_sender_email(message)
        sender_nick = self.__bot.get_sender_nick(message)
        yield f"@{sender_nick}: Granting {sender_email} access to resources in role '{role_name}' for {self.__bot.config['GRANT_TIMEOUT']} minutes"
