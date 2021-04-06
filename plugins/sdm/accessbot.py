from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re
import strongdm

from lib import access_helper, callback_message_helper, help_helper
import properties 

class AccessBot(BotPlugin):
    access_requests_status = {}

    def callback_message(self, message):
        """
        Callback for handling all messages
        """
        self.get_callback_message_helper().execute(
            admin_id = self.build_identifier(properties.get().admin()),
            grant_access_request_fn = self._grant_access_request,
            message = message
        )
            
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
        yield from self.get_access_helper().execute( 
            admin_id = self.build_identifier(properties.get().admin()),
            send_fn = self.send,
            is_access_request_granted_fn = self._is_access_request_granted,
            add_thumbsup_reaction_fn = self._add_thumbsup_reaction,
            enter_access_request_fn = self._enter_access_request,
            remove_access_request_fn = self._remove_access_request,
            message = message, 
            match_string = match.string
        )

    def get_access_helper(self):
        return access_helper

    def get_help_helper(self):
        return help_helper

    def get_callback_message_helper(self):
        return callback_message_helper

    def _is_access_request_granted(self, access_request_id):
        return self.access_requests_status[access_request_id] == 'APPROVED'

    def _grant_access_request(self, access_request_id):
        self.access_requests_status[access_request_id] = 'APPROVED'

    def _enter_access_request(self, access_request_id):
        self.access_requests_status[access_request_id] = 'PENDING'

    def _remove_access_request(self, access_request_id):
        self.access_requests_status.pop(access_request_id, None)

    def _add_thumbsup_reaction(self, message):
        if self._bot.mode == "slack":
            self._bot.add_reaction(message, "thumbsup")
