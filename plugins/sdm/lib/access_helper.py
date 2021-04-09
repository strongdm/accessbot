import datetime
import re
import shortuuid
import strongdm
import time

from .access_service import AccessService

def create_access_service(props):
    client = strongdm.Client(props.api_access_key(), props.api_secret_key())
    return AccessService(client)

class AccessHelper:
    def __init__(self, props):
        self.props = props
        self.access_service = create_access_service(props)

    def execute(self, admin_id, send_fn, is_access_request_granted_fn, add_thumbsup_reaction_fn, enter_access_request_fn, 
            remove_access_request_fn, message, match_string):
        resource_name = re.sub("^access to (.+)$", "\\1", match_string)
        sender_nick = self._get_sender_nick(message)
        sender_email = self._get_sender_email(message)

        try:
            sdm_resource = self.access_service.get_resource_by_name(resource_name)
            sdm_account = self.access_service.get_account_by_email(sender_email)

            access_request_id = self.generate_access_request_id()
            enter_access_request_fn(access_request_id)
            yield from self._notify_access_request_entered(send_fn, admin_id, sender_nick, resource_name, access_request_id)
            self._wait_before_check()
            if not is_access_request_granted_fn(access_request_id):
                yield from self._notify_access_request_denied(send_fn, admin_id)
                remove_access_request_fn(access_request_id)
                return

            self._grant_1hour_access(sdm_resource.id, sdm_account.id)
            add_thumbsup_reaction_fn(message)
            yield from self._notify_access_request_granted(sender_nick, sender_email, resource_name)
        except Exception as ex:
            yield str(ex)  

    def _get_sender_nick(self, message):
        if self.props.sender_override():
            return self.props.sender_nick()
        return '' if message.frm.nick is None else str(message.frm.nick)

    def _get_sender_email(self, message):
        if self.props.sender_override():
            return self.props.sender_email()
        return '' if message.frm.email is None else str(message.frm.email)

    def generate_access_request_id(self):
        return shortuuid.ShortUUID().random(length=4)

    def _notify_access_request_entered(self, send_fn, admin_id, sender_nick, resource_name, access_request_id):
        yield f"Thanks @{sender_nick}, that is a valid request. " + r"Let me check with the team admins! Your access request id is \`" + access_request_id + r"\`"
        send_fn(admin_id, r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + 
            r"\`! To approve, enter: **yes " + access_request_id + r"**")

    def _notify_access_request_denied(self, send_fn, admin_id):
        send_fn(admin_id, "Request timed out, user access will be denied!")
        yield "Sorry, not approved! Please contact your SDM admin directly."

    def _notify_access_request_granted(self, sender_nick, sender_email, resource_name):
        yield f"@{sender_nick}: Granting {sender_email} access to '{resource_name}' for 1 hour"
        
    def _wait_before_check(self):
        time.sleep(self.props.admin_timeout())

    def _grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        grant_valid_until = grant_start_from + datetime.timedelta(hours=1)
        self.access_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)