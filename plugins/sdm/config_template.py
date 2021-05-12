import os

_INSTANCE = {
    'ADMIN_TIMEOUT': int(os.getenv("SDM_ADMIN_TIMEOUT", "30")),
    'SENDER_NICK_OVERRIDE': os.getenv("SDM_SENDER_NICK_OVERRIDE"),
    'SENDER_EMAIL_OVERRIDE': os.getenv("SDM_SENDER_EMAIL_OVERRIDE"),
    'AUTO_APPROVE_ALL': str(os.getenv("SDM_AUTO_APPROVE_ALL", "")).lower() == 'true',
    'AUTO_APPROVE_TAG': os.getenv("SDM_AUTO_APPROVE_TAG"),
    'HIDE_RESOURCE_TAG': os.getenv("SDM_HIDE_RESOURCE_TAG"),
    'GRANT_TIMEOUT': int(os.getenv("SDM_GRANT_TIMEOUT", "60")),
}

def get():
    return _INSTANCE
