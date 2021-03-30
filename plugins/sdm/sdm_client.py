import strongdm

from properties import get_properties

props = get_properties()
_INSTANCE = strongdm.Client(props.sdm_api_access_key(), props.sdm_api_secret_key())

def create_client():
    return _INSTANCE
