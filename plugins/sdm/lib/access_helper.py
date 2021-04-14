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
    def __init__(self, props, admin_id, send_fn, is_access_request_granted_fn, add_thumbsup_reaction_fn, 
            enter_access_request_fn, remove_access_request_fn):
        self.__props = props
        self.__admin_id  = admin_id
        self.__send = send_fn
        self.__is_access_request_granted = is_access_request_granted_fn
        self.__add_thumbsup_reaction = add_thumbsup_reaction_fn
        self.__enter_access_request = enter_access_request_fn
        self.__remove_access_request = remove_access_request_fn
        self.access_service = create_access_service(props)

    def execute(self, message, match_string):
        resource_name = re.sub("^access to (.+)$", "\\1", match_string)
        sender_nick = self.__get_sender_nick(message)
        sender_email = self.__get_sender_email(message)

        try:
            sdm_resource = self.access_service.get_resource_by_name(resource_name)
            sdm_account = self.access_service.get_account_by_email(sender_email)

            if not self.__props.auto_approve_all():
                request_approved = yield from self.__ask_for_and_validate_approval(sender_nick, resource_name)
                if not request_approved: return

            self.__grant_1hour_access(sdm_resource.id, sdm_account.id)
            self.__add_thumbsup_reaction(message)
            yield from self.__notify_access_request_granted(sender_nick, sender_email, resource_name)
        except Exception as ex:
            yield str(ex)  

    def generate_access_request_id(self):
        return shortuuid.ShortUUID().random(length=4)

    def __get_sender_nick(self, message):
        if self.__props.sender_override():
            return self.__props.sender_nick()
        return '' if message.frm.nick is None else str(message.frm.nick)

    def __get_sender_email(self, message):
        if self.__props.sender_override():
            return self.__props.sender_email()
        return '' if message.frm.email is None else str(message.frm.email)

    def __ask_for_and_validate_approval(self, sender_nick, resource_name):
        access_request_id = self.generate_access_request_id()
        self.__enter_access_request(access_request_id)
        yield from self.__notify_access_request_entered(sender_nick, resource_name, access_request_id)
        
        self.__wait_before_check() 

        is_access_request_granted = self.__is_access_request_granted(access_request_id)
        self.__remove_access_request(access_request_id)
        if is_access_request_granted: 
            return True
        yield from self.__notify_access_request_denied()
        return False

    def __notify_access_request_entered(self, sender_nick, resource_name, access_request_id):
        yield f"Thanks @{sender_nick}, that is a valid request. " + r"Let me check with the team admins! Your access request id is \`" + access_request_id + r"\`"
        self.__send(self.__admin_id, r"Hey I have an access request from USER \`" + sender_nick + r"\` for RESOURCE \`" + resource_name + 
            r"\`! To approve, enter: **yes " + access_request_id + r"**")

    def __notify_access_request_denied(self):
        self.__send(self.__admin_id, "Request timed out, user access will be denied!")
        yield "Sorry, not approved! Please contact your SDM admin directly."

    def __notify_access_request_granted(self, sender_nick, sender_email, resource_name):
        yield f"@{sender_nick}: Granting {sender_email} access to '{resource_name}' for 1 hour"
        
    def __wait_before_check(self):
        time.sleep(self.__props.admin_timeout())

    def __grant_1hour_access(self, resource_id, account_id):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        grant_valid_until = grant_start_from + datetime.timedelta(hours=1)
        self.access_service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
