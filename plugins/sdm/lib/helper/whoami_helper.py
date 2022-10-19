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
        resp += f"| person    | `{frm.person}`\n"
        resp += f"| nick      | `{frm.nick}`\n"
        resp += f"| fullname  | `{frm.fullname}`\n"
        resp += f"| client    | `{frm.client}`\n"
        resp += f"| email     | `{self.__bot.get_sender_email(frm)}`\n\n"
        resp += self.__get_sdm_account_info(message)
        resp += self.__get_platform_info(message)
        resp += f"- User string representation is '{frm}'\n"
        if hasattr(frm, "room") and frm.room is not None:
            resp += f"`- room` is {frm.room}\n"
        resp += f"- User class is '{frm.__class__.__name__}'\n"
        return resp

    def __get_sdm_account_info(self, message):
        sdm_account = self.__bot.get_sdm_account(message)
        if sdm_account is None or len(sdm_account.tags.keys()) == 0:
            return ''
        info = "* SDM Account tags: "
        for index, (tag, value) in enumerate(sdm_account.tags.items()):
            if index > 0:
                info += ", "
            info += f"`{tag}: {value}`"
        info += "\n"
        return info

    def __get_platform_info(self, message):
        return self.__bot.get_platform_whoami_user_info(message.frm)
