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

    def stale_max_auto_approve_cleaner(self):
        max_auto_approve_interval = self.__bot.config['MAX_AUTO_APPROVE_INTERVAL']
        if not max_auto_approve_interval:
            return
        auto_approve_uses_counter = self.__bot.increase_auto_approve_uses_counter()
        if auto_approve_uses_counter >= (max_auto_approve_interval * 60):
            self.__bot.clean_auto_approve_uses()

    def __notify_grant_request_denied(self, grant_request):
        requester_id = grant_request['message'].frm
        self.__notify_admins(f"Request {grant_request['id']} timed out, user grant will be denied!")
        self.__notify_requester(requester_id, f"Sorry, request {grant_request['id']} not approved! Please contact any of the team admins directly.")

    def __get_channel_id(self, requester_id):
        if not hasattr(requester_id, 'room'):
            return None
        return self.__bot.build_identifier(f"#{requester_id.room.name}")

    def __notify_admins(self, message):
        for admin_id in self.__admin_ids:
            self.__bot.send(admin_id, message)

    def __notify_requester(self, requester_id, message):
        channel_id = self.__get_channel_id(requester_id)
        if channel_id:
            self.__bot.send(channel_id, message)
            return
        self.__bot.send(requester_id, message)
