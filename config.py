import os

CORE_PLUGINS=('ACLs', 'Health', 'Help', 'Plugins', 'Utils')
BACKEND = 'Slack'

BOT_DATA_DIR = 'data'
BOT_EXTRA_PLUGIN_DIR = 'plugins'

BOT_LOG_FILE = '' if str(os.getenv("SDM_DOCKERIZED", "")).lower() == 'true' else 'errbot.log'
BOT_LOG_LEVEL = os.getenv("LOG_LEVEL", 'INFO')

BOT_ADMINS = os.getenv("SDM_ADMINS").split(" ")
CHATROOM_PRESENCE = ()
BOT_IDENTITY = {
    'token': os.getenv("SLACK_TOKEN")
}

ACCESS_CONTROLS = {
    'AccessBot:approve': { 'allowusers': BOT_ADMINS },
    'AccessBot:*': { 'allowusers': ('*') },
    'help': { 'allowusers': ('*') },
    'whoami': { 'allowusers': ('*') },
    '*': { 'allowusers': BOT_ADMINS },
}

BOT_PREFIX = ''
HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True
DIVERT_TO_PRIVATE = ('help', 'AccessBot:approve')
