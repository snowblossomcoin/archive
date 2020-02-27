from . import Capability


class Path(Capability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node = None

    def update(self, node):
        self._node = node

    def get_mappings(self):
        return {'path': self}

    def nodes(self):
        try:
            return self._node.parent.path.nodes() + [self._node]
        except AttributeError:
            return [self._node]

    def depth(self):
        return len(self.nodes()) - 1
