from . import Capability
from .log import Log


class RecursiveMethod(Capability):
    def __init__(self, key, method_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node = None
        self._key = key
        self._method_name = method_name

    def update(self, node):
        self._node = node

    def get_mappings(self):
        return {self._key: self}

    @Log.decorator
    def recurse(self, *args, **kwargs):
        # call the method expected of each recurse
        if hasattr(self._node, self._method_name):
            self._node.log.log(5, f"{self._method_name}(args={ args }, kwargs={ kwargs })")
            getattr(self._node, self._method_name)(*args, **kwargs)
        else:
            try:
                self._node.log.log(5, f"{self._method_name} not available.")
            except AttributeError:
                pass

        # recurse through the node's children, if capable
        for child in self._node.children:
            recurse_capability = getattr(child, self._key)
            if recurse_capability:
                recurse_capability.recurse(*args, **kwargs)
