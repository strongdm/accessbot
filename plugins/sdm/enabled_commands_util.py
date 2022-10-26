import os
import re

def get_commands_enabled():
    return os.getenv("SDM_COMMANDS_ENABLED", "access_resource assign_role show_resources show_roles approve deny").split(" ")

def get_commands_aliases():
    commands_enabled = get_commands_enabled()
    aliases = {}
    for command_with_alias in commands_enabled:
        command_match = re.findall(r'[\w-]+', command_with_alias)
        command = command_match[0] if len(command_match) else None
        alias_match = re.findall(r'(?<=:)[\w-]+', command_with_alias)
        alias = alias_match[0] if len(alias_match) else None
        aliases[command] = alias
    return aliases
