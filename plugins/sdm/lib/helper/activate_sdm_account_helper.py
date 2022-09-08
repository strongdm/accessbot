class ActivateSDMAccountHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self, service_account_name: str):
        service_account = self.__sdm_service.get_account_by_name(service_account_name)
        if service_account.suspended:
            self.__sdm_service.reinstate_account(service_account)
        return service_account
