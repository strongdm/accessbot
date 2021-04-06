import re

ACCESS_REQUEST_GRANT_REGEX = "^yes ([a-z0-9]+)$"

class CallbackMessageHelper:
    def execute(self, admin_id, message):
        # TODO Move this logic to a helper method?
        # - Use a callback_helper 
        if self._is_valid_access_request_grant(admin_id, message):
            access_request_id = self._get_access_request_id(message)
            bot.access_requests_status[access_request_id] = 'APPROVED'

    def _is_valid_access_request_grant(self, admin_id, message):
        message_from_admin = message.frm == admin_id
        valid_grant_pattern = re.match(ACCESS_REQUEST_GRANT_REGEX, message.body, flags=re.I)
        return message_from_admin and valid_grant_pattern

    def _get_access_request_id(self, message):
        return re.sub(ACCESS_REQUEST_GRANT_REGEX, "\\1", message.body, flags=re.I)

