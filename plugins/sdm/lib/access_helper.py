import datetime
import re
import time
import shortuuid

from .access_service import create_access_service

class AccessHelper:
    def __init__(self, props, admin_ids, send_fn, is_access_request_granted_fn, add_thumbsup_reaction_fn,
            enter_access_request_fn, remove_access_request_fn):
        self.__props = props
        self.__admin_ids  = admin_ids
        self.__send = send_fn
        self.__is_access_request_granted = is_access_request_granted_fn
        self.__add_thumbsup_reaction = add_thumbsup_reaction_fn
        self.__enter_access_request = enter_access_request_fn
        self.__remove_access_request = remove_access_request_fn
        self.access_service = create_access_service(props)

    # pylint: disable=broad-except
    def execute(self, message, match_string):
        resource_name = re.sub("^access to (.+)$", "\\1", match_string)
        sender_nick = self.__get_sender_nick(message)
        sender_email = self.__get_sender_email(message)

        try:
            sdm_resource = self.access_service.get_resource_by_name(resource_name)
            sdm_account = self.access_service.get_account_by_email(sender_email)

            if self.__needs_manual_approval(sdm_resource):
                request_approved = yield from self.__ask_for_and_validate_approval(sender_nick, resource_name)
                if not request_approved:
                    return

            self.__grant_1hour_access(sdm_resource.id, sdm_account.id)
            self.__add_thumbsup_reaction(message)
            yield from self.__notify_access_request_granted(sender_nick, sender_email, resource_name)
        except Exception as ex:
            yield str(ex)

    @staticmethod
    def generate_access_request_id():
        return shortuuid.ShortUUID().random(length=4)

    def __get_sender_nick(self, message):
        override = self.__props.sender_nick_override()
        return override if override else str(message.frm.nick)

    def __get_sender_email(self, message):
        override = self.__props.sender_email_override()
        return override if override else str(message.frm.email)

    def __needs_manual_approval(self, sdm_resource):
        tagged_resource = self.__props.auto_approve_tag() is not None and self.__props.auto_approve_tag() in sdm_resource.tags
        return not self.__props.auto_approve_all() and not tagged_resource

    def __ask_for_and_validate_approval(self, sender_nick, resource_name):
        access_request_id = self.generate_access_request_id()
        self.__enter_access_request(access_request_id)
        yield from self.__notify_access_request_entered(sender_nick, resource_name, access_request_id)

        for _ in range(self.__props.admin_timeout()):
            time.sleep(1)
            is_access_request_granted = self.__is_access_request_granted(access_request_id)
            if is_access_request_granted:
                break

        self.__remove_access_request(access_request_id)
        if is_access_request_granted:
            return True
        yield from self.__notify_access_request_denied()
        return False

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__send(admin_id, message)

    def __notify_access_request_entered(self, sender_nick, resource_name, access_request_id):
        team_admins = ", ".join(self.__props.admins())
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
