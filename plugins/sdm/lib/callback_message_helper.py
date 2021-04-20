import re

ACCESS_REQUEST_GRANT_REGEX = "^.{0,2}yes ([a-z0-9]+).{0,2}$"

class CallbackMessageHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids(bot.get_properties().admins())

    def execute(self, message):
        if self.__is_valid_access_request(message):
            access_request_id = self.__get_access_request_id(message)
            self.__bot.grant_access_request(access_request_id)

    def __is_valid_access_request(self, message):
        message_from_admin = message.frm in self.__admin_ids
        valid_grant_pattern = re.match(ACCESS_REQUEST_GRANT_REGEX, message.body, flags=re.I) is not None
        is_valid_access_request = message_from_admin and valid_grant_pattern
        admin_ids = [a.person for a in self.__admin_ids]
        self.__bot.log.debug(
            "************** CallbackMessageHelper.__is_valid_access_request sender_id: %s sender_message: %s admin _ids: %s valid_access_request: %r",
            message.frm, message.body, admin_ids, is_valid_access_request
        )
        return is_valid_access_request

    def __get_access_request_id(self, message):
        return re.sub(ACCESS_REQUEST_GRANT_REGEX, "\\1", message.body, flags=re.I)
