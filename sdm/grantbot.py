from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import strongdm, datetime, re, time, os
from datetime import timezone, timedelta

# Get config settings from env
admin_timeout = os.getenv("SDM_ADMIN_TIMEOUT", "30")
admin1 = os.getenv("SDM_ADMIN")
access_key = os.getenv("SDM_API_ACCESS_KEY")
secret_key = os.getenv("SDM_API_SECRET_KEY")

client = strongdm.Client(access_key, secret_key)

class Grantbot(BotPlugin):

    def callback_message(self, mess):
        if mess.body == "yes" and mess.frm == self.build_identifier(admin1):
            self['Approved'] = "true"

    """
    Grants access to strongDM resources
    """
    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """
        self['Approved'] = "false"
        email = message.frm.email
        result = re.sub('^access to (.+)$','\\1',match.string)        
        start = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
        end = start + timedelta(hours=1)
        slack_result = ''

        try:
            resources = list(client.resources.list('name:"{}"'.format(result ) ) )
        except Exception as ex:
            yield "List resources failed: " + str(ex)
        else:
            if len(resources) > 0:
                resID = resources[0].id
            else:
                yield "Sorry, cannot find that resource!"
                return
        
        try:
            users = list(client.accounts.list('email:{}'.format(email)))
        except Exception as ex:
            yield "List users failed: " + str(ex)
        else:
            if len(users) > 0:
                userID = users[0].id
            else:
                yield "Sorry, cannot find your account!"
                return
             
        myGrant = strongdm.AccountGrant(resource_id='{}'.format(resID),account_id='{}'.format(userID),start_from=start, valid_until=end)
        
        yield "Thanks " + "@" + message.frm.nick + ", that is a valid request. Let me check with the team admins!"
        approval = self.send(
            self.build_identifier(admin1), "Hey I have an access request from USER \`" + message.frm.nick + "\` for RESOURCE \`" + result + "\`! Enter 'yes' to approve.",)
        time.sleep(10)
        if self['Approved'] == "false":
            approval = self.send(
            self.build_identifier(admin1), "Request timed out, user will be denied access!",)
            yield "Sorry, not approved! Please contact your SDM admin directly."
            return

        try:
            respGrant = client.account_grants.create(myGrant)
        except Exception as ex:
            yield "Grant failed: " + str(ex)
            return
        else:
            if self._bot.mode == "slack":
                self._bot.add_reaction(message, "thumbsup")
            slack_result = "@" + message.frm.nick + " : Granting " + email + " access to '" + result + "' for 1 hour"
        
        yield slack_result
        return
    