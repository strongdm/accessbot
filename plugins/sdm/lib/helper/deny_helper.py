from .base_evaluate_request_helper import BaseEvaluateRequestHelper

class DenyHelper(BaseEvaluateRequestHelper):
    def evaluate(self, request_id, **kwargs):
        grant_request = self._bot.get_grant_request(request_id)
        self._bot.remove_grant_request(request_id)
        yield from self.__notify_access_request_denied(kwargs['admin'], kwargs['reason'], grant_request)

    def __notify_access_request_denied(self, admin, denial_reason, grant_request):
        requester = grant_request['message'].frm
        sdm_object_name = grant_request['sdm_object'].name
        sender_email = self._bot.get_sender_email(requester)
        sender_nick = self._bot.get_sender_nick(requester)
        admin_nick = self._bot.get_sender_nick(admin)
        denial_message = f"Your request **{grant_request['id']}** has been denied by admin {admin_nick}"
        if denial_reason:
            denial_message += f' with the following reason: "{denial_reason}"'
        self.__notify_requester(requester, grant_request['message'], denial_message)
        yield f"{sender_nick}: Denying {sender_email} access to '{sdm_object_name}'"

    def __notify_requester(self, requester_id, message, text):
        channel_id = self.__get_channel_id(requester_id)
        if channel_id:
            self._bot.send(channel_id, text, in_reply_to=message)
            return
        self._bot.send(requester_id, text, in_reply_to=message)

    def __get_channel_id(self, requester_id):
        if not hasattr(requester_id, 'room'):
            return None
        return self._bot.build_identifier(f"#{requester_id.room.name}")
