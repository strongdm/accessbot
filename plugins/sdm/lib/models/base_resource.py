from typing import Dict


class BaseResource:
    def __init__(self, dictionary: Dict) -> None:
        for key, value in dictionary.items():
            setattr(self, key, value)

    def to_dict(self):
        return self.__dict__
