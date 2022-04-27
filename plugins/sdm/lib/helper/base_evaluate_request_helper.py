import shortuuid
from abc import ABC, abstractmethod

class BaseEvaluateRequestHelper(ABC):
    def __init__(self, bot):
        self._bot = bot

    def execute(self, user, request_id, reason=''):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute request_id: %s", execution_id, request_id)

        if not self._bot.is_valid_grant_request_id(request_id):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute invalid access request id: %s", execution_id, request_id)
            yield f"Invalid access request id = {request_id}"
            return

        if not self.__is_allowed_to_evaluate(request_id, user):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute Invalid user, not an admin to self approve or deny: %s", execution_id, str(user))
            yield "Invalid user, not an admin to self approve or deny"
            return

        if not self.__is_admin(user):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute Invalid user, not an admin: %s", execution_id, str(user))
            yield "Invalid user, not an admin or using the wrong channel"
            return

        self._bot.log.info("##SDM## %s EvaluateRequestHelper.execute concluding evaluation for access request id: %s", execution_id, request_id)
        yield from self.evaluate(request_id, admin=user, reason=reason)

    def __is_allowed_to_evaluate(self, request_id, evaluator):
        grant_request = self._bot.get_grant_request(request_id)
        is_self_approve = grant_request['sdm_account'].email == evaluator.email
        return not is_self_approve or self._bot.get_user_nick(evaluator) in self._bot.get_admins()

    def __is_admin(self, evaluator):
        admins_channel = self._bot.config['ADMINS_CHANNEL']
        evaluator_channel = None if not hasattr(evaluator, 'room') else f"#{evaluator.room.name}"
        if admins_channel:
            return evaluator_channel == admins_channel
        return self._bot.get_sender_id(evaluator) in self._bot.get_admins()

    def _notify_requester(self, requester_id, message, text):
        channel_id = self.__get_channel_id(requester_id)
        if channel_id:
            self._bot.send(channel_id, text, in_reply_to=message)
            return
        self._bot.send(requester_id, text, in_reply_to=message)

    def __get_channel_id(self, requester_id):
        if not hasattr(requester_id, 'room'):
            return None
        return self._bot.build_identifier(f"#{requester_id.room.name}")

    @abstractmethod
    def evaluate(request_id, **kwargs):
        pass
