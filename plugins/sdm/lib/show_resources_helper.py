from .access_service import create_access_service

def _get_key(sdm_resource):
    return sdm_resource.name

class ShowResourcesHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.access_service = create_access_service(bot.get_api_access_key(), bot.get_api_secret_key(), bot.log)

    def execute(self):
        resources = "Available resources:\n\n"
        sdm_resources = self.get_resources()
        for sdm_resource in sorted(sdm_resources, key = _get_key):
            hide_resource = self.__bot.config['HIDE_RESOURCE_TAG'] is not None and self.__bot.config['HIDE_RESOURCE_TAG'] in sdm_resource.tags
            if hide_resource:
                continue
            resources += self.get_resource_line(sdm_resource)
        yield resources

    def get_resources(self):
        role_name = self.__bot.config['CONTROL_RESOURCES_ROLE_NAME']
        if role_name is not None:
            return self.access_service.get_all_resources_by_role(role_name)
        return self.access_service.get_all_resources()

    def get_resource_line(self, sdm_resource):
        auto_approve = self.__bot.config['AUTO_APPROVE_TAG'] is not None and self.__bot.config['AUTO_APPROVE_TAG'] in sdm_resource.tags
        if auto_approve:
            return f"* **{sdm_resource.name} (type: {type(sdm_resource).__name__}, auto-approve)**\n"
        return f"* {sdm_resource.name} (type: {type(sdm_resource).__name__})\n"
