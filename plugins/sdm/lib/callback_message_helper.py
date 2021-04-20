import re
import shortuuid

ACCESS_REQUEST_GRANT_REGEX = "^.{0,2}yes ([a-z0-9]+).{0,2}$"

class CallbackMessageHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids(bot.get_properties().admins())

    def execute(self, message):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug(
            "**SDM** %s CallbackMessageHelper.execute sender_id: %s sender_message: %s admin _ids: %s",
            execution_id, message.frm, message.body, [a.person for a in self.__admin_ids]
        )

        if not self.__is_valid_access_request(message):
            self.__bot.log.debug("**SDM** %s CallbackMessageHelper.execute ignoring message, invalid access request approval", execution_id)
            return

        access_request_id = self.__get_access_request_id(message)
        if not self.__bot.is_valid_access_request_id(access_request_id):
            self.__bot.log.debug("**SDM** %s CallbackMessageHelper.execute invalid access request id: %s", execution_id, access_request_id)
            return
        self.__bot.approve_access_request(access_request_id)
        self.__bot.log.info("**SDM** %s CallbackMessageHelper.execute approving access to request id: %s", execution_id, access_request_id)

    def __is_valid_access_request(self, message):
        message_from_admin = message.frm in self.__admin_ids
        valid_grant_pattern = re.match(ACCESS_REQUEST_GRANT_REGEX, message.body, flags=re.I) is not None
        return message_from_admin and valid_grant_pattern

    def __get_access_request_id(self, message):
        return re.sub(ACCESS_REQUEST_GRANT_REGEX, "\\1", message.body, flags=re.I)
