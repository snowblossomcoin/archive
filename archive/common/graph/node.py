from archive.common.graph.capabilities.capability import Capability


class Node:
    def __init__(self, name=None, parent=None, capabilities=None, children=None):
        self.name = name or self.__class__.__name__.lower()
        self.parent = parent
        self.children = []
        self._capabilities = []
        self._capability_map = {}

        self.add_capabilities(capabilities)
        self.add_children(children)

    def __repr__(self):
        return self.name

    def update(self):
        for capability in self._capabilities:
            capability.update(self)
            self._capability_map.update(**capability.get_mappings())

        for child in self.children:
            child.update()

    def add_children(self, children):
        if children:
            if not isinstance(children, list):
                children = [children]

            for child in children:
                child.parent = self
                child.update()
                self.children.append(child)

    def add_capabilities(self, capabilities: list):
        if capabilities:
            for capability in capabilities:
                if not isinstance(capability, Capability):
                    capability = capability()
                capability.update(self)
                self._capability_map.update(**capability.get_mappings())
                self._capabilities.append(capability)

    def has_capability(self, capability: Capability):
        return capability in self._capability_map

    def __getattr__(self, item):
        try:
            return self._capability_map[item]
        except KeyError:
            raise AttributeError(f"Attribute or Capability '{item}' not found.")
