from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import datetime, re, time
from datetime import timezone, timedelta
import strongdm

from access_service import AccessService
from bot_support import help_message
from properties import props

def create_access_service():
    client = strongdm.Client(props.sdm_api_access_key(), props.sdm_api_secret_key())
    return AccessService(client)
    
class AccessBot(BotPlugin):
    service = create_access_service()
    props = props

    def callback_message(self, mess):
        # TODO Make this check case insensitive 
        if mess.body == "yes" and mess.frm == self.build_identifier(self.props.admin()):
            self.approved = True

    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        A command for showing help
        """
        yield help_message

    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """        
        # TODO Fix possible race conditions introduced by this flag
        self.approved = False

        resource_name = re.sub("^access to (.+)$", "\\1", match.string)
        admin_slack_id =  self.build_identifier(self.props.admin())

        # TODO Default value introduced for testing - mock and remove check
        sender_email = "" if message.frm.email is None else str(message.frm.email)
        sender_nick = "" if message.frm.nick is None else str(message.frm.nick)

        try:
            sdm_resource = self.service.get_resource_by_name(resource_name)
            sdm_account = self.service.get_account_by_email(sender_email)

            yield f"Thanks @{sender_nick}, that is a valid request. Let me check with the team admins!"
            self.send(admin_slack_id, r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + r"\`! Enter 'yes' to approve.")
            self.wait_before_check()
            if not self.approved:
                self.send(admin_slack_id, "Request timed out, user will be denied access!")
                yield "Sorry, not approved! Please contact your SDM admin directly."
                return

            self.grant_1hour_access(sdm_resource.id, sdm_account.id)
            self.add_thumbsup(message)
            yield f"@{sender_nick} : Granting {sender_email} access to '{resource_name}' for 1 hour"
        except Exception as ex:
            yield str(ex)
        
    def wait_before_check(self):
        time.sleep(self.props.admin_timeout())

    def grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
        grant_valid_until = grant_start_from + timedelta(hours=1)
        self.service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)

    def add_thumbsup(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")


