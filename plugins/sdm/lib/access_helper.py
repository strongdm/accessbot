import shortuuid

class AccessHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__access_service = bot.get_access_service()

    # pylint: disable=broad-except
    def execute(self, message, resource_name):
        execution_id = shortuuid.ShortUUID().random(length=6)
        sender_nick = self.__bot.get_sender_nick(message)
        sender_email = self.__bot.get_sender_email(message)

        self.__bot.log.info(
            "##SDM## %s AccessHelper.execute new access request for resource_name: %s sender_nick: %s sender_email: %s",
            execution_id, resource_name, sender_nick, sender_email
        )
        try:
            sdm_resource = self.__access_service.get_resource_by_name(resource_name)
            if self.__is_hidden_resource(sdm_resource):
                self.__bot.log.debug("##SDM## %s AccessHelper.execute hidden resource", execution_id)
                yield "Invalid resource name"
                return

            sdm_account = self.__access_service.get_account_by_email(sender_email)
            access_request_id = self.__create_access_request(message, sdm_resource, sdm_account)

            if self.__needs_manual_approval(sdm_resource):
                yield from self.__notify_access_request_entered(sender_nick, resource_name, access_request_id)
                self.__bot.log.debug("##SDM## %s AccessHelper.execute needs manual approval", execution_id)
                return

            self.__bot.log.info("##SDM## %s AccessHelper.execute granting access", execution_id)
            yield from self.__bot.get_approve_helper().approve(access_request_id)
        except Exception as ex:
            self.__bot.log.error("##SDM## %s AccessHelper.execute access request failed %s", execution_id, str(ex))
            yield str(ex)

    @staticmethod
    def generate_access_request_id():
        return shortuuid.ShortUUID().random(length=4)

    def __is_hidden_resource(self, sdm_resource):
        return self.__bot.config['HIDE_RESOURCE_TAG'] is not None and self.__bot.config['HIDE_RESOURCE_TAG'] in sdm_resource.tags

    def __create_access_request(self, message, sdm_resource, sdm_account):
        access_request_id = self.generate_access_request_id()
        self.__bot.enter_access_request(access_request_id, message, sdm_resource, sdm_account)
        return access_request_id

    def __needs_manual_approval(self, sdm_resource):
        tagged_resource = self.__bot.config['AUTO_APPROVE_TAG'] is not None and self.__bot.config['AUTO_APPROVE_TAG'] in sdm_resource.tags
        return not self.__bot.config['AUTO_APPROVE_ALL'] and not tagged_resource

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__bot.send(admin_id, message)

    def __notify_access_request_entered(self, sender_nick, resource_name, access_request_id):
        team_admins = ", ".join(self.__bot.get_admins())
        yield f"Thanks @{sender_nick}, that is a valid request. Let me check with the team admins: {team_admins}\n" + r"Your access request id is \`" + access_request_id + r"\`"
        self.__notify_admins(r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + r"\`! To approve, enter: **yes " + access_request_id + r"**")
