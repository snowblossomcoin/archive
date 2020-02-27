

class CapabilityDependencyException(Exception):
    pass


class Capability:
    def __init__(self, *args, **kwargs):
        pass

    def update(self, node):
        pass

    def get_mappings(self):
        return {}
