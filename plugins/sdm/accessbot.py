from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re
import strongdm

from lib import AccessHelper, CallbackMessageHelper, help_helper
import properties 

class AccessBot(BotPlugin):
    __access_requests_status = {}

    def callback_message(self, message):
        """
        Callback for handling all messages
        """
        self.get_callback_message_helper().execute(message)
            
    @re_botcmd(pattern=r"^help", prefixed=False, flags=re.IGNORECASE)
    def help(self, message, match):
        """
        Command for showing help
        """
        yield from self.get_help_helper().execute()

    @re_botcmd(pattern=r"^access to (.+)$", prefixed=False, flags=re.IGNORECASE)
    def access(self, message, match):
        """
        Command which grants access to the named SDM resource.
        """
        yield from self.get_access_helper().execute(message, match.string)

    def get_access_helper(self):
        props = properties.get()
        return AccessHelper(
            props = props, 
            admin_id = self.build_identifier(props.admin()),
            send_fn = self.send,
            is_access_request_granted_fn = self.__is_access_request_granted,
            add_thumbsup_reaction_fn = self.__add_thumbsup_reaction,
            enter_access_request_fn = self.__enter_access_request,
            remove_access_request_fn = self.__remove_access_request
        )

    def get_help_helper(self):
        return help_helper

    def get_callback_message_helper(self):
        return CallbackMessageHelper(
            admin_id = self.build_identifier(properties.get().admin()),
            grant_access_request_fn = self.grant_access_request
        )

    def is_access_request_granted(self, access_request_id):
        return self.__access_requests_status[access_request_id] == 'APPROVED'

    def grant_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'APPROVED'

    def enter_access_request(self, access_request_id):
        self.__access_requests_status[access_request_id] = 'PENDING'

    def remove_access_request(self, access_request_id):
        self.__access_requests_status.pop(access_request_id, None)

    def add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
