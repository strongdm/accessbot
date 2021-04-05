import logging, os, sys

sys.path.append('plugins/sdm')
import properties
props = properties.get()

BACKEND = 'Slack'  

BOT_DATA_DIR = r'data'
BOT_EXTRA_PLUGIN_DIR = r'plugins'

BOT_LOG_FILE = r'errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = (props.admin())
CHATROOM_PRESENCE = ()
BOT_IDENTITY = {
    'token': props.slack_token()
}
