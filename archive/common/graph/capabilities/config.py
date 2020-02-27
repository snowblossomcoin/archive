from . import Capability


class Config(Capability):
    def __init__(self, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = config

    def update(self, node):
        try:
            self._config = node.parent.config
        except AttributeError:
            pass

    def get_mappings(self):
        return {"config": self._config}
