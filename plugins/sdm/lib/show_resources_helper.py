from .access_service import create_access_service

def _get_key(sdm_resource):
    return sdm_resource.name

class ShowResourcesHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.access_service = create_access_service(bot.get_api_access_key(), bot.get_api_secret_key(), bot.log)

    def execute(self):
        resources = "Available resources:\n\n"
        sdm_resources = self.access_service.get_all_resources()
        for sdm_resource in sorted(sdm_resources, key = _get_key):
            auto_approve = self.__bot.config['AUTO_APPROVE_TAG'] is not None and self.__bot.config['AUTO_APPROVE_TAG'] in sdm_resource.tags
            hide_resource = self.__bot.config['HIDE_RESOURCE_TAG'] is not None and self.__bot.config['HIDE_RESOURCE_TAG'] in sdm_resource.tags
            if hide_resource:
                continue
            if auto_approve:
                resources += f"* **{sdm_resource.name} (type: {type(sdm_resource).__name__}, auto-approve)**\n"
            else:
                resources += f"* {sdm_resource.name} (type: {type(sdm_resource).__name__})\n"
        yield resources
