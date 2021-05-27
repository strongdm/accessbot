def _get_key(sdm_role):
    return sdm_role.name

class ShowRolesHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self):
        roles = "Available roles:\n\n"
        sdm_roles = self.__sdm_service.get_all_roles()
        for sdm_role in sorted(sdm_roles, key = _get_key):
            roles += f"* {sdm_role.name}\n"
        yield roles
