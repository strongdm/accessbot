from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import strongdm, datetime, re
from datetime import timezone, timedelta

access_key="key"
secret_key="secret"
client = strongdm.Client(access_key, secret_key)

class Grantbot(BotPlugin):
    """
    Grants access to strongDM resources
    """
    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)

    def access(self, message, match):
        """
        A command which grants access to the named SDM resource.
        """
        email = message.frm.email
        result = re.sub('^access to (.+)$','\\1',match.string)        
        start = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
        end = start + timedelta(hours=1)
        slack_result = ''

        try:
            resources = list(client.resources.list('name:"{}"'.format(result ) ) )
        except Exception as ex:
            return "List resources failed"
        else:
            if len(resources) > 0:
                resID = resources[0].id
            else:
                return "Sorry, cannot find that resource!"
        
        try:
            users = list(client.accounts.list('email:{}'.format(email)))
        except Exception as ex:
            return "List users failed"
        else:
            if len(users) > 0:
                userID = users[0].id
            else:
                return "Sorry, cannot find your account!"
 
        myGrant = strongdm.AccountGrant(resource_id='{}'.format(resID),account_id='{}'.format(userID),start_from=start, valid_until=end)
        try:
            respGrant = client.account_grants.create(myGrant)
        except Exception as ex:
            return "Grant failed"
        else:
            if self._bot.mode == "slack":
                self._bot.add_reaction(message, "sdm")
            slack_result = "@" + message.frm.nick + ":Granting " + email + " access to '" + result + "' for 1 hour"
        
        return slack_result
    