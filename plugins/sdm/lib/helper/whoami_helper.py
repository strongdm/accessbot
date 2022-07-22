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
        resp += f"| email     | `{self.__bot.get_sender_email(frm)}`\n"
        if hasattr(frm, "room"):
            resp += f"\n`room` is {frm.room}\n"
        resp += f"\n\n- string representation is '{frm}'\n"
        resp += f"- class is '{frm.__class__.__name__}'\n"
        return resp
