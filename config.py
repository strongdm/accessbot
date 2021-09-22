import os

def get_access_controls():
    commands_enabled = os.getenv("SDM_COMMANDS_ENABLED", "access_resource assign_role show_resources show_roles approve").split(" ")
    allow_all = { 'allowusers': ('*') }
    deny_all = { 'denyusers': ('*') }
    return { # The order in this dict matters!
        'AccessBot:access_resource': allow_all if 'access_resource' in commands_enabled else deny_all,
        'AccessBot:approve': allow_all if 'approve' in commands_enabled else deny_all,
        'AccessBot:assign_role': allow_all if 'assign_role' in commands_enabled else deny_all,
        'AccessBot:show_resources': allow_all if 'show_resources' in commands_enabled else deny_all,
        'AccessBot:show_roles': allow_all if 'show_roles' in commands_enabled else deny_all,
        'help': { 'allowusers': ('*') },
        'whoami': { 'allowusers': ('*') },
        '*': { 'allowusers': BOT_ADMINS },
    }

CORE_PLUGINS=('ACLs', 'Health', 'Help', 'Plugins', 'Utils')

BACKEND = 'SlackBolt'
BOT_EXTRA_BACKEND_DIR = 'errbot-slack-bolt-backend/errbot_slack_bolt_backend'

BOT_DATA_DIR = 'data'
BOT_EXTRA_PLUGIN_DIR = 'plugins'

BOT_LOG_FILE = '' if str(os.getenv("SDM_DOCKERIZED", "")).lower() == 'true' else 'errbot.log'
BOT_LOG_LEVEL = os.getenv("LOG_LEVEL", 'INFO')

BOT_ADMINS = os.getenv("SDM_ADMINS").split(" ")
CHATROOM_PRESENCE = ()
BOT_IDENTITY = {
    "app_token": os.environ["SLACK_APP_TOKEN"],
    "bot_token": os.environ["SLACK_BOT_TOKEN"],
}

ACCESS_CONTROLS = get_access_controls()

BOT_PREFIX = ''
HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True
