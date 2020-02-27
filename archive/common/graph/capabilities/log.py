from . import Capability
import logging


class Log(Capability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log = logging.getLogger()

    def update(self, node):
        try:
            self._log = node.parent.log.getChild(node.name)
        except AttributeError:
            self._log = logging.getLogger(node.name)

    def get_mappings(self):
        return {'log': self._log}

    @classmethod
    def decorator(self, f, *args, **kwargs):
        def new_f(self, *args, **kwargs):
            if isinstance(self, Capability):
                if self._node and self._node.has_capability(Log):
                    self.log.debug(f"{f.__name__}")
            else:
                self.log.debug(f"{f.__name__}")
            return f(self, *args, **kwargs)
        return new_f
