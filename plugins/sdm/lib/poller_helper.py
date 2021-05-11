import time

class PollerHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()

    def stale_access_requests_cleaner(self):
        for ar_id in list(self.__bot['access_requests'].keys()):
            elapsed_time = time.time() - self.__bot['access_requests'][ar_id]['timestamp']
            if elapsed_time > self.__bot.config['ADMIN_TIMEOUT']:
                self.__bot.log.info("##SDM## Cleaning access requests, stale access_request_id = %s", ar_id)
                self.__bot.remove_access_request(ar_id)

