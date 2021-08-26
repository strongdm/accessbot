def _get_key(sdm_role):
    return sdm_role.name

# Refactor: Implement a BaseShowHelper
class ShowRolesHelper:
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()

    def execute(self, message):
        roles = "Available roles:\n\n"
        sdm_roles = self.__sdm_service.get_all_roles()
        account = self.__get_account(message)
        permitted_roles = account.tags.get(self.__bot.config['USER_ROLES_TAG'])
        if permitted_roles is not None:
            permitted_roles = permitted_roles.split(',')
        for sdm_role in sorted(sdm_roles, key = _get_key):
            # Refactor: Make easier to read this horrible nested conditions
            if permitted_roles is None or sdm_role.name in permitted_roles:
                if self.__bot.config['AUTO_APPROVE_ROLE_TAG'] in sdm_role.tags:
                    roles += r"* **" + sdm_role.name + r" (auto-approve)**" + "\n"
                else:
                    roles += f"* {sdm_role.name}\n"
            else:
                roles += r"* ~" + sdm_role.name + r"~" + " (not allowed) \n"
        yield roles

    def __get_account(self, message):
        sender_email = self.__bot.get_sender_email(message.frm)
        return self.__sdm_service.get_account_by_email(sender_email)
