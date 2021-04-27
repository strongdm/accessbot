import shortuuid

class ApproveHelper:
    def __init__(self, bot):
        self.__bot = bot

    def execute(self, access_request_id):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug("**SDM** %s ApproveHelper.execute access_request_id: %s", execution_id, access_request_id)

        if not self.__bot.is_valid_access_request_id(access_request_id):
            self.__bot.log.debug("**SDM** %s ApproveHelper.execute invalid access request id: %s", execution_id, access_request_id)
            yield f"Invalid access request id = {access_request_id}"

        self.__bot.approve_access_request(access_request_id)
        self.__bot.log.info("**SDM** %s ApproveHelper.execute approving access to request id: %s", execution_id, access_request_id)
        yield
