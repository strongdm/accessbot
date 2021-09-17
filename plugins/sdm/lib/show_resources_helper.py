from .util import is_hidden_resource
from .base_show_helper import BaseShowHelper

class ShowResourcesHelper(BaseShowHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()
        super().__init__("resources")

    def get_list(self):
        role_name = self.__bot.config["CONTROL_RESOURCES_ROLE_NAME"]
        if role_name is not None:
            resources = self.__sdm_service.get_all_resources_by_role(role_name)
        else:
            resources = self.__sdm_service.get_all_resources()
        return self.__filter_hidden_resources(resources)

    def get_line(self, item, message = ''):
        auto_approve = (
            self.__bot.config["AUTO_APPROVE_TAG"] is not None
            and self.__bot.config["AUTO_APPROVE_TAG"] in item.tags
        )
        if auto_approve:
            return f"* **{item.name} (type: {type(item).__name__}, auto-approve)**\n"
        return f"* {item.name} (type: {type(item).__name__})\n"

    def __filter_hidden_resources(self, resources):
        return [
            resource
            for resource in resources
            if not is_hidden_resource(self.__bot.config, resource)
        ]
