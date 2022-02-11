import re

class CommandAliasHelper:
    regex_group_request_id = "(\\w{4})"

    def __init__(self, bot):
        self.__bot = bot

    def execute(self, message):
        if not hasattr(self.__bot.bot_config, 'BOT_COMMANDS_ALIASES'):
            return

        for command, alias in self.__bot.bot_config.BOT_COMMANDS_ALIASES.items():
            if alias is None:
                continue
            if self.__alias_matches(command, alias, message.body):
                yield from self.__invoke_method_from_command(command, message, alias)
                break

    def __alias_matches(self, command, alias, text):
        alias_regex = self.__build_alias_regex(command, alias)
        alias_compiled_regex = re.compile(alias_regex)
        alias_match = alias_compiled_regex.match(text)
        return alias_match is not None

    def __get_original_regex_from_command(self, command):
        return getattr(self.__bot, command)._err_command_syntax

    def __build_alias_regex(self, command, alias):
        request_id_regex = self.__get_request_id_regex(command)
        argument_regex = self.__get_command_argument_regex(command)
        return r'^' + alias + request_id_regex + argument_regex + r'$'

    def __get_request_id_regex(self, command):
        full_command_regex = self.__get_original_regex_from_command(command)
        command_expects_request_id = self.regex_group_request_id in full_command_regex
        return r' (\w{4})' if command_expects_request_id else ''

    def __get_command_argument_regex(self, command):
        full_command_regex = self.__get_original_regex_from_command(command)
        if '(.+)?' in full_command_regex:
            return r' ?(.+)?'
        elif '(.+)' in full_command_regex:
            return r' (.+)'
        return r''

    def __invoke_method_from_command(self, command, message, alias):
        message.body = self.__convert_alias_message_to_full_command_message(alias, command, message)
        match = self.__get_full_command_message_match(command, message.body)
        command_method = getattr(self.__bot, command)
        yield from command_method(message, match)

    def __convert_alias_message_to_full_command_message(self, alias, command, message):
        alias_regex = self.__build_alias_regex(command, alias)
        full_command_regex = self.__get_original_regex_from_command(command)
        converted_message = full_command_regex
        command_expects_request_id = self.regex_group_request_id in full_command_regex
        if command_expects_request_id:
            request_id = self.__extract_value_from_regex_group(alias_regex, r"\1", message.body)
            converted_message = converted_message.replace(self.regex_group_request_id, request_id)
        command_expects_argument = '(.+)' in full_command_regex
        if command_expects_argument:
            argument_regex_group = r"\1" if not command_expects_request_id else r"\2"
            argument = self.__extract_value_from_regex_group(alias_regex, argument_regex_group, message.body)
            converted_message = converted_message.replace('?', '').replace('(.+)', argument)
        return converted_message

    def __extract_value_from_regex_group(self, regex, extract_regex_group, text):
        return re.sub(regex, extract_regex_group, text)

    def __get_full_command_message_match(self, command, text):
        full_command_regex = self.__get_original_regex_from_command(command)
        method_regex_compiled = re.compile(full_command_regex)
        return method_regex_compiled.match(text)
