import logging, os

BACKEND = 'Slack'  

BOT_DATA_DIR = r'data'
BOT_EXTRA_PLUGIN_DIR = r'plugins'

BOT_LOG_FILE = r'errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = (os.getenv("SDM_ADMIN"))
CHATROOM_PRESENCE = ()
BOT_IDENTITY = {
    'token': os.getenv('SLACK_TOKEN', '')
}
