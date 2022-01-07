import os

def get_access_controls():
    commands_enabled = os.getenv("SDM_COMMANDS_ENABLED", "access_resources assign_role show_resources show_roles approve").split(" ")
    allow_all = { 'allowusers': ('*') }
    deny_all = { 'denyusers': ('*') }
    return { # The order in this dict matters!
        'AccessBot:access_resources': allow_all if 'access_resources' in commands_enabled else deny_all,
        'AccessBot:approve': allow_all if 'approve' in commands_enabled else deny_all,
        'AccessBot:assign_role': allow_all if 'assign_role' in commands_enabled else deny_all,
        'AccessBot:show_resources': allow_all if 'show_resources' in commands_enabled else deny_all,
        'AccessBot:show_roles': allow_all if 'show_roles' in commands_enabled else deny_all,
        'help': { 'allowusers': ('*') },
        'whoami': { 'allowusers': ('*') },
        '*': { 'allowusers': BOT_ADMINS },
    }

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


CORE_PLUGINS = ('ACLs', 'Health', 'Help', 'Plugins', 'Utils', 'Webserver')

BACKEND = get_backend()
BOT_EXTRA_BACKEND_DIR = get_bot_extra_backend_dir()

BOT_DATA_DIR = 'data'
BOT_EXTRA_PLUGIN_DIR = 'plugins'

BOT_PLATFORM = os.getenv("SDM_BOT_PLATFORM")

BOT_LOG_FILE = '' if str(os.getenv("SDM_DOCKERIZED", "")).lower() == 'true' else 'errbot.log'
BOT_LOG_LEVEL = os.getenv("LOG_LEVEL", 'INFO')

BOT_ADMINS = os.getenv("SDM_ADMINS").split(" ")
CHATROOM_PRESENCE = ()
BOT_IDENTITY = get_bot_identity()

ACCESS_CONTROLS = get_access_controls()

BOT_PREFIX = ''
HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True
