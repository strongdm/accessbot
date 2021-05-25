import pickle
import time

class PollerHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()

    def stale_access_requests_cleaner(self):
        for access_request_id in self.__bot.get_grant_request_ids():
            access_request = self.__bot.get_grant_request(access_request_id)
            elapsed_time = time.time() - access_request['timestamp']
            if elapsed_time > self.__bot.config['ADMIN_TIMEOUT']:
                self.__bot.log.info("##SDM## Cleaning access requests, stale access_request_id = %s", access_request_id)
                self.__notify_access_request_denied(access_request)
                self.__bot.remove_grant_request(access_request_id)

    def __notify_access_request_denied(self, access_request):
        self.__notify_admins(f"Request {access_request['id']} timed out, user access will be denied!")
        self.__notify_requester(access_request, f"Sorry, request {access_request['id']} not approved! Please contact any of the team admins directly.")

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__bot.send(admin_id, message)

    def __notify_requester(self, access_request, message):
        requester_id = access_request['message'].frm
        self.__bot.send(requester_id, message)