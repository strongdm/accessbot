import strongdm

import properties

_INSTANCE = None
def get_instance(props = properties.get()):
    global _INSTANCE
    if not _INSTANCE:
        _INSTANCE = strongdm.Client(props.sdm_api_access_key(), props.sdm_api_secret_key())
    return _INSTANCE

