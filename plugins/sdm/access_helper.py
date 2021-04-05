import datetime
import re
import strongdm
import time

from access_service import AccessService

def create_access_service(props):
    client = strongdm.Client(props.sdm_api_access_key(), props.sdm_api_secret_key())
    return AccessService(client)

class AccessHelper:
    def __init__(self, props):
        self.props = props
        self.access_service = create_access_service(props)

    def execute(self, bot, message, match):
        # TODO Fix possible race conditions introduced by this flag
        bot.approved = False

        resource_name = re.sub("^access to (.+)$", "\\1", match.string)
        admin_slack_id =  bot.build_identifier(self.props.admin())

        # TODO Default value introduced for testing - mock and remove check
        sender_nick = "" if message.frm.nick is None else str(message.frm.nick)
        sender_email = "" if message.frm.email is None else str(message.frm.email)

        try:
            sdm_resource = self.access_service.get_resource_by_name(resource_name)
            sdm_account = self.access_service.get_account_by_email(sender_email)

            yield f"Thanks @{sender_nick}, that is a valid request. Let me check with the team admins!"
            bot.send(admin_slack_id, r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + r"\`! Enter 'yes' to approve.")
            self.wait_before_check()
            if not bot.approved:
                bot.send(admin_slack_id, "Request timed out, user will be denied access!")
                yield "Sorry, not approved! Please contact your SDM admin directly."
                return

            self.grant_1hour_access(sdm_resource.id, sdm_account.id)
            self.add_thumbsup(bot, message)
            yield f"@{sender_nick} : Granting {sender_email} access to '{resource_name}' for 1 hour"
        except Exception as ex:
            yield str(ex)
        
    def wait_before_check(self):
        time.sleep(self.props.admin_timeout())

    def grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        grant_valid_until = grant_start_from + datetime.timedelta(hours=1)
        self.access_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)

    def add_thumbsup(self, bot, message):
        if bot._bot.mode == "slack":
            bot._bot.add_reaction(message, "thumbsup")
