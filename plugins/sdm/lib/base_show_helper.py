from abc import ABC, abstractmethod

class BaseShowHelper(ABC):
    def __init__(self, data_name):
        self.__data_name = data_name

    def execute(self, message = ''):
        resources = f"Available {self.__data_name}:\n\n"
        data = self.get_list()
        for item in sorted(data, key=self.__get_key):
            resources += self.get_line(item, message)
        yield resources

    @abstractmethod
    def get_list(self):
        pass

    @abstractmethod
    def get_line(self, item, message=""):
        pass

    def __get_key(self, item):
        return item.name
