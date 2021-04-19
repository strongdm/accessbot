import re

ACCESS_REQUEST_GRANT_REGEX = "^yes ([a-z0-9]+)$"

class CallbackMessageHelper:
    def __init__(self, log, admin_ids, grant_access_request_fn):
        self.__log = log
        self.__admin_ids = admin_ids
        self.__grant_access_request = grant_access_request_fn

    def execute(self, message):
        if self.__is_valid_access_request(message):
            access_request_id = self.__get_access_request_id(message)
            self.__grant_access_request(access_request_id)

    def __is_valid_access_request(self, message):
        message_from_admin = message.frm in self.__admin_ids
        valid_grant_pattern = re.match(ACCESS_REQUEST_GRANT_REGEX, message.body, flags=re.I) is not None
        is_valid_access_request_grant = message_from_admin and valid_grant_pattern
        admin_ids = [a.person for a in self.__admin_ids]
        self.__log.info(f"************** sender_id: {message.frm} sender_message: {message.body}  admin _ids: {admin_ids} is_valid_access_request: {is_valid_access_request_grant}")
        return is_valid_access_request_grant

    def __get_access_request_id(self, message):
        return re.sub(ACCESS_REQUEST_GRANT_REGEX, "\\1", message.body, flags=re.I)
