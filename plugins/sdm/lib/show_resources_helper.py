from .access_service import create_access_service

def _get_key(sdm_resource):
    return sdm_resource.name

class ShowResourcesHelper:
    def __init__(self, bot):
        self.__props = bot.get_properties()
        self.access_service = create_access_service(bot.get_properties(), bot.log)

    def execute(self):
        resources = "Available resources:\n\n"
        sdm_resources = self.access_service.get_all_resources()
        for sdm_resource in sorted(sdm_resources, key = _get_key):
            auto_approve = self.__props.auto_approve_tag() is not None and self.__props.auto_approve_tag() in sdm_resource.tags
            hide_resource = self.__props.hide_resource_tag() is not None and self.__props.hide_resource_tag() in sdm_resource.tags
            if hide_resource:
                continue
            if auto_approve:
                resources += f"* **{sdm_resource.name} (type: {type(sdm_resource).__name__}, auto-approve)**\n"
            else:
                resources += f"* {sdm_resource.name} (type: {type(sdm_resource).__name__})\n"
        yield resources
