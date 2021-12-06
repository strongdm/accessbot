from abc import ABC, abstractmethod

class BaseShowHelper(ABC):
    def __init__(self, op_desc):
        self.__op_desc = op_desc

    def execute(self, message = '', filter = ''):
        data = self.get_list(filter)
        if len(data):
            resources = f"Available {self.__op_desc}:\n\n"
            for item in sorted(data, key=self.__get_key):
                resources += self.get_line(item, message)
            yield resources
            return
        yield f"There are no available {self.__op_desc}"

    @abstractmethod
    def get_list(self, filter):
        pass

    @abstractmethod
    def get_line(self, item, message):
        pass

    @abstractmethod
    def is_auto_approve(self, item):
        pass

    def __get_key(self, item):
        return item.name
