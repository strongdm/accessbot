from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import datetime, re, time
from datetime import timezone, timedelta

import access_service
from properties import get_properties
import sdm_client

class Grantbot(BotPlugin):
    client = sdm_client.create_client()
    service = access_service.create_service()
    props = get_properties()

    def callback_message(self, mess):
        if mess.body == "yes" and mess.frm == self.build_identifier(self.props.admin()):
            self.approved = True

    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        A command for showing help
        """
        yield self.service.help()

    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """
        # TODO Validate possible race conditions introduced by this flag
        self.approved = False
        
        resource_name = re.sub("^access to (.+)$", "\\1", match.string)
        admin_slack_id =  self.build_identifier(self.props.admin())
        grant_start_from = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
        grant_valid_until = grant_start_from + timedelta(hours=1)

        # TODO Default value introduced for testing, mock and remove
        sender_email = "" if message.frm.email is None else str(message.frm.email)
        sender_nick = "" if message.frm.nick is None else str(message.frm.nick)

        try:
            sdm_resource = self.service.get_resource_by_name(resource_name)
            sdm_account = self.service.get_account_by_email(sender_email)

            yield f"Thanks @{sender_nick}, that is a valid request. Let me check with the team admins!"
            self.send(admin_slack_id, f"Hey I have an access request from USER `{sender_nick}` for RESOURCE `{resource_name}`! Enter 'yes' to approve.")
            time.sleep(10)
            if not self.approved:
                self.send(admin_slack_id, "Request timed out, user will be denied access!")
                yield "Sorry, not approved! Please contact your SDM admin directly."
                return

            self.service.grant_temporary_access(resource.id, account.id, grant_start_from, grant_valid_until)
            self.add_thumbsup(message)
            yield f"@{sender_nick} : Granting {sender_email} access to '{resource_name}' for 1 hour"
        except Exception as ex:
            yield str(ex)
        

    def add_thumbsup(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
