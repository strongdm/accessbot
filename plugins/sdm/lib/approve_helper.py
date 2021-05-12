import datetime
import shortuuid

class ApproveHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__access_service = bot.get_access_service()

    def execute(self, access_request_id):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug("##SDM## %s ApproveHelper.execute access_request_id: %s", execution_id, access_request_id)

        if not self.__bot.is_valid_access_request_id(access_request_id):
            self.__bot.log.debug("##SDM## %s ApproveHelper.execute invalid access request id: %s", execution_id, access_request_id)
            yield f"Invalid access request id = {access_request_id}"
            return

        self.__bot.log.info("##SDM## %s ApproveHelper.execute approving access to request id: %s", execution_id, access_request_id)
        yield from self.approve(access_request_id)

    def approve(self, access_request_id):
        access_request = self.__bot.get_access_request(access_request_id)
        self.__grant_1hour_access(access_request['sdm_resource'].id, access_request['sdm_account'].id)
        self.__bot.add_thumbsup_reaction(access_request['message'])
        self.__bot.remove_access_request(access_request_id)
        yield from self.__notify_access_request_granted(access_request['message'], access_request['sdm_resource'].name)

    def __grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(hours=1)
        self.__access_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)

    def __notify_access_request_granted(self, message, resource_name):
        sender_email = self.__bot.get_sender_email(message)
        sender_nick = self.__bot.get_sender_nick(message)
        yield f"@{sender_nick}: Granting {sender_email} access to '{resource_name}' for 1 hour"
