import logging


class PlatformMetaClient:
    def __init__(self, credentials, path, online=True, parent_logger=None, *args, **kwargs):
        self.credentials = credentials
        self.client = None
        self.path = path
        self.online = online
        self.__users = None
        self.__channels = None
        if parent_logger:
            self.log = parent_logger.getChild(self.__class__.__name__.lower())
        else:
            self.log = logging.getLogger(self.__class__.__name__.lower())

    @property
    def users(self):
        return None

    @property
    def channels(self):
        return None
