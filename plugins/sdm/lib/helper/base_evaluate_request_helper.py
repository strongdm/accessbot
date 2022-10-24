import shortuuid
from abc import ABC, abstractmethod

from ..platform.ms_teams_platform import MSTeamsPlatform
from ..util import get_approvers_channel


class BaseEvaluateRequestHelper(ABC):
    def __init__(self, bot):
        self._bot = bot

    def execute(self, user, request_id, reason=''):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute request_id: %s", execution_id, request_id)

        if not self._bot.grant_requests_exists(request_id):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute invalid access request id: %s", execution_id, request_id)
            yield f'Invalid access request id = "{request_id}"'
            return

        if not self.__is_allowed_to_self_evaluate(request_id, user):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute Invalid user, not an admin to self approve or deny: %s", execution_id, str(user))
            yield "Invalid user, not an admin to self approve or deny"
            return

        if not self.__is_allowed_to_evaluate(request_id, user):
            self._bot.log.debug("##SDM## %s EvaluateRequestHelper.execute Invalid user, not an admin or using the wrong channel: %s", execution_id, str(user))
            yield "Invalid user, not an admin or using the wrong channel"
            return

        self._bot.log.info("##SDM## %s EvaluateRequestHelper.execute concluding evaluation for access request id: %s", execution_id, request_id)
        yield from self.evaluate(request_id, admin=user, reason=reason)

    def __is_allowed_to_self_evaluate(self, request_id, evaluator):
        grant_request = self._bot.get_grant_request(request_id)
        is_self_approve = grant_request['sdm_account'].email == evaluator.email
        return not is_self_approve or self._bot.get_user_nick(evaluator) in self._bot.get_admins()

    def __is_allowed_to_evaluate(self, request_id, evaluator):
        grant_request = self._bot.get_grant_request(request_id)
        sdm_account = grant_request['sdm_account']
        sdm_object = grant_request['sdm_object']
        approvers_channel = get_approvers_channel(self._bot.config, sdm_object) or get_approvers_channel(self._bot.config, sdm_account)
        if approvers_channel is not None:
            return self.__is_valid_approver_channel(evaluator, self._bot.format_channel_name(approvers_channel))
        return self.__is_admin(evaluator)

    def __is_valid_approver_channel(self, evaluator, approvers_channel):
        return self._bot.channel_match_str_rep(evaluator.room, approvers_channel)

    def __is_admin(self, evaluator):
        admins_channel = self._bot.config['ADMINS_CHANNEL']
        if admins_channel:
            return self._bot.channel_match_str_rep(evaluator.room, admins_channel)
        return self._bot.get_sender_id(evaluator).lower() in self._bot.get_admins()

    def _notify_requester(self, requester_id, message, text):
        if hasattr(requester_id, 'room') and requester_id.room is not None:
            self._bot.send(requester_id.room, text, in_reply_to=message)
            return
        self._bot.send(requester_id, text, in_reply_to=message)

    @abstractmethod
    def evaluate(self, request_id, **kwargs):
        pass
