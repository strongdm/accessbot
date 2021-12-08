from .base_show_helper import BaseShowHelper
from ..util import is_hidden, HiddenTagEnum, is_concealed, AllowedTagEnum, is_allowed


class ShowResourcesHelper(BaseShowHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()
        super().__init__("resources")

    def get_list(self, filter):
        role_name = self.__bot.config["CONTROL_RESOURCES_ROLE_NAME"]
        if role_name is not None:
            resources = self.__sdm_service.get_all_resources_by_role(role_name, filter = filter)
        else:
            resources = self.__sdm_service.get_all_resources(filter = filter)
        return self.__filter_resources(resources)

    def get_line(self, item, message):
        if self.is_auto_approve(item):
            return f"* **{item.name} (type: {type(item).__name__}, auto-approve)**\n"
        details = [f'type: {type(item).__name__}']
        if self.has_auto_approve_groups(item):
            details.append(f'auto-approve: "{item.tags[self.__bot.config["AUTO_APPROVE_TAG"]]}"')
        return f"* {item.name} ({', '.join(details)})\n"

    def is_auto_approve(self, item):
        return (
            self.__bot.config["AUTO_APPROVE_TAG"] is not None
            and self.__bot.config["AUTO_APPROVE_TAG"] in item.tags
            and 'true' in item.tags[self.__bot.config["AUTO_APPROVE_TAG"]]
        )

    def has_auto_approve_groups(self, item):
        return (
            self.__bot.config["AUTO_APPROVE_TAG"] is not None
            and self.__bot.config["GROUPS_TAG"] is not None
            and self.__bot.config["AUTO_APPROVE_TAG"] in item.tags
            and item.tags[self.__bot.config["AUTO_APPROVE_TAG"]] is not None
            and len(str(item.tags[self.__bot.config["AUTO_APPROVE_TAG"]]))
        )

    def __filter_resources(self, resources):
        return [
            resource
            for resource in resources
            if not is_hidden(self.__bot.config, HiddenTagEnum.RESOURCE, resource)
            and not is_concealed(self.__bot.config, resource)
            and is_allowed(self.__bot.config, AllowedTagEnum.RESOURCE, resource)
        ]
