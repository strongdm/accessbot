from abc import ABC, abstractmethod

class BaseShowHelper(ABC):
    def __init__(self, bot, op_desc):
        self._bot = bot
        self._sdm_service = bot.get_sdm_service()
        self.__op_desc = op_desc

    def execute(self, message, flags: dict = {}):
        filter = flags.get('filter') or ''
        sdm_account = self.__get_sdm_account(message)
        data = self.get_list(filter, sdm_account)
        if len(data) == 0:
            yield f"There are no available {self.__op_desc}"
            return
        resources = f"Available {self.__op_desc}:\n\n"
        for item in sorted(data, key=self.__get_key):
            resources += self.get_line(item, sdm_account)
        yield resources

    @abstractmethod
    def get_list(self, filter, sdm_account):
        pass

    @abstractmethod
    def get_line(self, item, sdm_account):
        pass

    @abstractmethod
    def is_auto_approve(self, item):
        pass

    def __get_sdm_account(self, message):
        sender_email = self._bot.get_sender_email(message.frm)
        return self._sdm_service.get_account_by_email(sender_email)

    def __get_key(self, item):
        return item.name
