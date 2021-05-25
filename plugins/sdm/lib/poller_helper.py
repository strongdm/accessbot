import time

class PollerHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()

    def stale_grant_requests_cleaner(self):
        for request_id in self.__bot.get_grant_request_ids():
            grant_request = self.__bot.get_grant_request(request_id)
            elapsed_time = time.time() - grant_request['timestamp']
            if elapsed_time > self.__bot.config['ADMIN_TIMEOUT']:
                self.__bot.log.info("##SDM## Cleaning grant requests, stale request_id = %s", request_id)
                self.__notify_grant_request_denied(grant_request)
                self.__bot.remove_grant_request(request_id)

    def __notify_grant_request_denied(self, grant_request):
        self.__notify_admins(f"Request {grant_request['id']} timed out, user grant will be denied!")
        self.__notify_requester(grant_request, f"Sorry, request {grant_request['id']} not approved! Please contact any of the team admins directly.")

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__bot.send(admin_id, message)

    def __notify_requester(self, grant_request, message):
        requester_id = grant_request['message'].frm
        self.__bot.send(requester_id, message)