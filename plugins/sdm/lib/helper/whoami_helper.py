class WhoamiHelper:
    def __init__(self, bot) -> None:
        self.__bot = bot

    def execute(self, message):
        frm = message.frm
        resp = ""
        if self.__bot.bot_config.GROUPCHAT_NICK_PREFIXED:
            resp += "\n\n"
        resp += f"| key       | value\n"
        resp += f"| --------  | --------\n"
        resp += f"| fullname  | {frm.fullname}\n"
        resp += f"| nick      | {frm.nick}\n"
        resp += f"| email     | {self.__bot.get_sender_email(frm)}\n\n"
        resp += self.__get_sdm_account_info(message)
        resp += self.__get_platform_info(message)
        resp += f"- User string representation is '{frm}'\n"
        if hasattr(frm, "room") and frm.room is not None:
            resp += f"`- room` is {frm.room}\n"
        resp += f"- User class is '{frm.__class__.__name__}'\n"
        return resp

    def __get_sdm_account_info(self, message):
        try:
            sdm_account = self.__bot.get_sdm_account(message)
            if sdm_account is None:
                raise Exception('SDM Account not found')
        except:
            return '* SDM Account status: NOT FOUND\n'
        info = ''
        if sdm_account is not None and len(sdm_account.tags.keys()) > 0:
            info += "* SDM Account tags: "
            for index, (tag, value) in enumerate(sdm_account.tags.items()):
                if index > 0:
                    info += ", "
                info += f"`{tag}: {value}`"
            info += "\n"
        info += f"* SDM Account status: {'SUSPENDED' if sdm_account.suspended else 'ACTIVE'}\n"
        return info

    def __get_platform_info(self, message):
        return self.__bot.get_platform_whoami_user_info(message.frm)
