import logging

BACKEND = 'Slack'  

BOT_DATA_DIR = r'/errbot/data'
BOT_EXTRA_PLUGIN_DIR = r'/errbot/plugins'

BOT_LOG_FILE = r'/errbot/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG


# Change this to a Slack user in your org
BOT_ADMINS = ('@david')
CHATROOM_PRESENCE = ()
BOT_IDENTITY = {'token': 'REDACTED'}