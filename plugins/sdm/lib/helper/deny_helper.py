import shortuuid


class DenyHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self, user, request_id, denial_reason):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.debug("##SDM## %s DenyHelper.execute request_id: %s", execution_id, request_id)

        if not self.__bot.is_valid_grant_request_id(request_id):
            self.__bot.log.debug("##SDM## %s DenyHelper.execute invalid access request id: %s", execution_id, request_id)
            yield f"Invalid access request id = {request_id}"
            return

        if not self.__is_admin(user):
            self.__bot.log.debug("##SDM## %s DenyHelper.execute invalid user, not an admin: %s", execution_id, str(user))
            yield "Invalid user, not an admin or using the wrong channel"
            return

        self.__bot.log.info("##SDM## %s DenyHelper.execute denying access to request id: %s", execution_id, request_id)
        yield from self.deny(user, request_id, denial_reason)

    def deny(self, admin, request_id, denial_reason):
        grant_request = self.__bot.get_grant_request(request_id)
        self.__bot.remove_grant_request(grant_request['id'])
        yield from self.__notify_access_request_denied(admin, grant_request['message'], denial_reason, grant_request['sdm_object'].name)

    def __is_admin(self, user):
        admins_channel = self.__bot.config['ADMINS_CHANNEL']
        user_channel = None if not hasattr(user, 'room') else f"#{user.room.name}"
        if admins_channel:
            return user_channel == admins_channel
        return self.__bot.get_sender_id(user) in self.__bot.get_admins()

    def __notify_access_request_denied(self, admin, message, denial_reason, sdm_object_name):
        denial_message = f'Your request has been denied by admin {admin}'
        if denial_reason:
            denial_message += f' with the following reason: "{denial_reason}"'
        self.__bot.send(message.frm, denial_message)
        sender_email = self.__bot.get_sender_email(message.frm)
        sender_nick = self.__bot.get_sender_nick(message.frm)
        yield f"{sender_nick}: Denying {sender_email} access to '{sdm_object_name}'"
