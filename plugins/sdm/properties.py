import os

class Properties:
    def __init__(
        self, 
        admin_timeout, 
        admin, 
        sdm_api_access_key, 
        sdm_api_secret_key
    ):
        self._admin_timeout = int(admin_timeout)
        self._admin = admin
        self._sdm_api_access_key = sdm_api_access_key
        self._sdm_api_secret_key = sdm_api_secret_key

    def admin_timeout(self):
        return self._admin_timeout

    def admin(self):
        return self._admin

    def sdm_api_access_key(self):
        return self._sdm_api_access_key

    def sdm_api_secret_key(self):
        return self._sdm_api_secret_key


_INSTANCE = None
def get():
    global _INSTANCE
    if not _INSTANCE:
        _INSTANCE = Properties(
                        os.getenv("SDM_ADMIN_TIMEOUT", "30"),
                        os.getenv("SDM_ADMIN"), 
                        os.getenv("SDM_API_ACCESS_KEY"),
                        os.getenv("SDM_API_SECRET_KEY")
                    )
    return _INSTANCE
