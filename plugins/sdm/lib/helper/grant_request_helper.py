import copy
import json
import time
from collections import namedtuple
from os.path import isfile

from grant_request_type import GrantRequestType


class GrantRequestHelper:
    __grant_requests = {}
    file_path = "./data/grant_requests.json"

    def __init__(self, bot):
        self._bot = bot
        self.__restore_state()

    def __save_state(self):
        if self._bot.mode == 'test':
            return
        try:
            with open(self.file_path, "w") as state:
                grant_requests_list = []
                for grant_request in self.__grant_requests.values():
                    serializable_grant_request = {
                        'id': grant_request['id'],
                        'timestamp': grant_request['timestamp'],
                        'message': {
                            'frm': grant_request['message'].frm.__str__(),
                            'to': grant_request['message'].to.__str__(),
                            'extras': grant_request['message'].extras
                        },
                        'sdm_object': self.__sdm_model_to_dict(grant_request['sdm_object']),
                        'sdm_account': self.__sdm_model_to_dict(grant_request['sdm_account']),
                        'type': grant_request['type'],
                        'flags': grant_request['flags'],
                    }
                    grant_requests_list.append(serializable_grant_request)
                state.write(json.dumps(grant_requests_list))
        except Exception as e:
            self._bot.log.error("An error occurred while saving the grant requests state: ", str(e))

    def __restore_state(self):
        if self._bot.mode == 'test':
            return
        self.__grant_requests = {}
        if not isfile(self.file_path):
            return
        try:
            state_text = open(self.file_path, "r").read()
            if state_text == "":
                return
            grant_requests_list = json.loads(state_text)
            for grant_request in grant_requests_list:
                message_dict = {
                    'frm': self._bot.build_identifier(grant_request['message']['frm']),
                    'to': self._bot.build_identifier(grant_request['message']['to']),
                    'extras': grant_request['message'].get('extras')
                }
                grant_request['message'] = namedtuple('message', message_dict.keys())(*message_dict.values())
                self.__grant_requests[grant_request['id']] = grant_request
        except Exception as e:
            self._bot.log.error("An error occurred while restoring the grant requests state: ", str(e))

    def add(self, request_id: str, message, sdm_object, sdm_account, grant_request_type: GrantRequestType, flags: dict = None):
        self.__grant_requests[request_id] = {
            'id': request_id,
            'timestamp': time.time(),
            'message': message,
            'sdm_object': sdm_object,
            'sdm_account': sdm_account,
            'type': grant_request_type.value,
            'flags': flags,
        }
        self.__save_state()

    def get(self, request_id: str):
        return self.__grant_requests.get(request_id)

    def get_request_ids(self):
        return list(self.__grant_requests.keys())

    def exists(self, request_id: str) -> bool:
        return self.__grant_requests.get(request_id) is not None

    def remove(self, request_id: str):
        self.__grant_requests.pop(request_id, None)
        self.__save_state()

    def __sdm_model_to_dict(self, object):
        return object if type(object) is dict else object.to_dict()
