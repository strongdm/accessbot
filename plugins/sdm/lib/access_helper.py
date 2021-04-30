import datetime
import time
import shortuuid

from .access_service import create_access_service

class AccessHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.access_service = create_access_service(bot.get_api_access_key(), bot.get_api_secret_key(), bot.log)

    # pylint: disable=broad-except
    def execute(self, message, resource_name):
        execution_id = shortuuid.ShortUUID().random(length=6)
        sender_nick = self.__get_sender_nick(message)
        sender_email = self.__get_sender_email(message)

        self.__bot.log.info(
            "##SDM## %s AccessHelper.execute new access request for resource_name: %s sender_nick: %s sender_email: %s",
            execution_id, resource_name, sender_nick, sender_email
        )
        try:
            sdm_resource = self.access_service.get_resource_by_name(resource_name)
            if self.__is_hidden_resource(sdm_resource):
                self.__bot.log.debug("##SDM## %s AccessHelper.execute hidden resource", execution_id)
                yield "Invalid resource name"
                return

            sdm_account = self.access_service.get_account_by_email(sender_email)
            if self.__needs_manual_approval(sdm_resource):
                self.__bot.log.debug("##SDM## %s AccessHelper.execute needs manual approval", execution_id)
                request_approved = yield from self.__ask_for_and_validate_approval(sender_nick, resource_name)
                if not request_approved:
                    self.__bot.log.debug("##SDM## %s AccessHelper.execute request not approved", execution_id)
                    return

            self.__grant_1hour_access(sdm_resource.id, sdm_account.id)
            self.__bot.add_thumbsup_reaction(message)
            yield from self.__notify_access_request_granted(sender_nick, sender_email, resource_name)
            self.__bot.log.info("##SDM## %s AccessHelper.execute access request granted", execution_id)
        except Exception as ex:
            self.__bot.log.error("##SDM## %s AccessHelper.execute access request failed %s", execution_id, str(resource_name))
            yield str(ex)

    @staticmethod
    def generate_access_request_id():
        return shortuuid.ShortUUID().random(length=4)

    def __get_sender_nick(self, message):
        override = self.__bot.config['SENDER_NICK_OVERRIDE']
        return override if override else str(message.frm.nick)

    def __get_sender_email(self, message):
        override = self.__bot.config['SENDER_EMAIL_OVERRIDE']
        return override if override else str(message.frm.email)

    def __is_hidden_resource(self, sdm_resource):
        return self.__bot.config['HIDE_RESOURCE_TAG'] is not None and self.__bot.config['HIDE_RESOURCE_TAG'] in sdm_resource.tags

    def __needs_manual_approval(self, sdm_resource):
        tagged_resource = self.__bot.config['AUTO_APPROVE_TAG'] is not None and self.__bot.config['AUTO_APPROVE_TAG'] in sdm_resource.tags
        return not self.__bot.config['AUTO_APPROVE_ALL'] and not tagged_resource

    def __ask_for_and_validate_approval(self, sender_nick, resource_name):
        access_request_id = self.generate_access_request_id()
        self.__bot.enter_access_request(access_request_id)
        yield from self.__notify_access_request_entered(sender_nick, resource_name, access_request_id)

        for _ in range(self.__bot.config['ADMIN_TIMEOUT']):
            time.sleep(1)
            is_access_request_approved = self.__bot.is_access_request_approved(access_request_id)
            if is_access_request_approved:
                break

        self.__bot.remove_access_request(access_request_id)
        if is_access_request_approved:
            return True
        yield from self.__notify_access_request_denied()
        return False

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__bot.send(admin_id, message)

    def __notify_access_request_entered(self, sender_nick, resource_name, access_request_id):
        team_admins = ", ".join(self.__bot.get_admins())
        yield f"Thanks @{sender_nick}, that is a valid request. Let me check with the team admins: {team_admins}\n" + r"Your access request id is \`" + access_request_id + r"\`"
        self.__notify_admins(r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + r"\`! To approve, enter: **yes " + access_request_id + r"**")

    def __notify_access_request_denied(self):
        self.__notify_admins("Request timed out, user access will be denied!")
        yield "Sorry, not approved! Please contact any of the team admins directly."

    @staticmethod
    def __notify_access_request_granted(sender_nick, sender_email, resource_name):
        yield f"@{sender_nick}: Granting {sender_email} access to '{resource_name}' for 1 hour"

    def __grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        grant_valid_until = grant_start_from + datetime.timedelta(hours=1)
        self.access_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
