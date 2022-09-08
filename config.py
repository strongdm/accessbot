import os
import re

def get_commands_enabled():
    return os.getenv("SDM_COMMANDS_ENABLED", "access_resource assign_role show_resources show_roles approve deny assign_role_to_service_account").split(" ")

def is_admins_channel_elevate_enabled():
    return str(os.getenv("SDM_ADMINS_CHANNEL_ELEVATE", "")).lower() == 'true' and os.getenv("SDM_ADMINS_CHANNEL") is not None

def get_access_controls():
    commands_enabled = [re.sub(r':[\w-]+', '', cmd) for cmd in get_commands_enabled()]
    allow_all = { 'allowusers': ('*') }
    deny_all = { 'denyusers': ('*') }
    return { # The order in this dict matters!
        'AccessBot:access_resource': allow_all if 'access_resource' in commands_enabled else deny_all,
        'AccessBot:approve': allow_all if 'approve' in commands_enabled else deny_all,
        'AccessBot:assign_role': allow_all if 'assign_role' in commands_enabled else deny_all,
        'AccessBot:deny': allow_all if 'deny' in commands_enabled else deny_all,
        'AccessBot:show_resources': allow_all if 'show_resources' in commands_enabled else deny_all,
        'AccessBot:show_roles': allow_all if 'show_roles' in commands_enabled else deny_all,
        'AccessBot:assign_role_to_service_account': {
            'allowusers': BOT_ADMINS,
            'allowprivate': True,
            'allowmuc': False
        } if 'assign_role_to_service_account' in commands_enabled else deny_all,
        'AccessBot:match_alias': allow_all,
        'AccessBot:accessbot-whoami': {
            'allowusers': ('*'),
            'allowprivate': True,
            'allowmuc': False,
        },
        'help': { 'allowusers': ('*') },
        'whoami': deny_all,
        '*': {
            'allowusers': BOT_ADMINS,
            'allowrooms': [os.getenv('SDM_ADMINS_CHANNEL')],
            'allowprivate': not is_admins_channel_elevate_enabled(),
            'allowmuc': is_admins_channel_elevate_enabled(),
        },
    }

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

def get_bot_identity():
    platform = os.getenv('SDM_BOT_PLATFORM')
    if platform == 'ms-teams':
        return {
            "appId": os.getenv("AZURE_APP_ID"),
            "appPassword": os.getenv("AZURE_APP_PASSWORD")
        }
    elif platform == 'slack-classic':
        return {
            'token': os.getenv("SLACK_TOKEN")
        }
    return {
        "app_token": os.getenv("SLACK_APP_TOKEN"),
        "bot_token": os.getenv("SLACK_BOT_TOKEN"),
    }

def get_backend():
    platform = os.getenv('SDM_BOT_PLATFORM')
    if platform == 'ms-teams':
        return 'BotFramework'
    elif platform == 'slack-classic':
        return 'Slack'
    return 'SlackBolt'

def get_bot_extra_backend_dir():
    platform = os.getenv('SDM_BOT_PLATFORM')
    if platform == 'ms-teams':
        return 'errbot-backend-botframework'
    elif platform == 'slack-classic':
        return None
    return 'errbot-slack-bolt-backend/errbot_slack_bolt_backend'

def get_bot_admins():
    return os.getenv("SDM_ADMINS").split(" ")

CORE_PLUGINS = ('ACLs', 'Backup', 'ChatRoom', 'CommandNotFoundFilter', 'Flows', 'Health', 'Help', 'Plugins', 'TextCmds',
                'Utils', 'VersionChecker', 'Webserver')

BACKEND = get_backend()
BOT_EXTRA_BACKEND_DIR = get_bot_extra_backend_dir()

BOT_DATA_DIR = 'data'
BOT_EXTRA_PLUGIN_DIR = 'plugins'

BOT_PLATFORM = os.getenv("SDM_BOT_PLATFORM")

BOT_LOG_FILE = '' if str(os.getenv("SDM_DOCKERIZED", "")).lower() == 'true' else 'errbot.log'
BOT_LOG_LEVEL = os.getenv("LOG_LEVEL", 'INFO')

BOT_ADMINS = get_bot_admins()
CHATROOM_PRESENCE = ()
BOT_IDENTITY = get_bot_identity()

ACCESS_CONTROLS = get_access_controls()

BOT_PREFIX = ''
HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True

BOT_COMMANDS_ALIASES = get_commands_aliases()

ACCESS_FORM_BOT_INFO = {
    "bot_id": None,  # will be initialized in SlackBoltBackend.resolve_access_form_bot_id method
    "nickname": os.getenv("SDM_ACCESS_FORM_BOT_NICKNAME")
}

EXPOSE_METRICS = os.getenv("SDM_EXPOSE_METRICS", "false").lower() == "true"
