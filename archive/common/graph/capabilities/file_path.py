from . import Capability
from pathlib import Path
import json
import shutil


class FilePath(Capability):
    def __init__(
            self,
            key: str = "relative_file_path",
            base_path: (str, Path) = None,
            is_file: bool = False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._node = None
        self._key = key
        self._base_path = base_path and Path(base_path)
        self._is_file = is_file

    def update(self, node):
        self._node = node

    def get_mappings(self):
        return {self._key: self}

    def __call__(self, *args, **kwargs):
        return self.path()

    def path(self):
        if self._base_path:
            return self._base_path
        elif self._node.parent and self._node.parent.has_capability(self._key):
            path = getattr(self._node.parent, self._key).path()
            if not self._is_file:
                path /= self._node.name
            return path
        else:
            return Path(self._node.name)

    def nodes(self):
        if not self._base_path and self._node.parent and self._node.parent.has_capability(self._key):
            nodes = getattr(self._node.parent, self._key).nodes()
            if not self._is_file:
                nodes += [self._node]
            return nodes
        return [self._node]

    def depth(self):
        if not self._base_path and self._node.parent and self._node.parent.has_capability(self._key):
            depth = getattr(self._node.parent, self._key).depth()
            if not self._is_file:
                depth += 1
            return depth
        return 0

    def copy(self, path, new_path=''):
        self.path().mkdir(parents=True, exist_ok=True)
        shutil.copy(str(path), str(self.path() / new_path))

    def save(self, filename, thing):
        path = self.path() / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(thing)

        try:
            self._node.log.debug(f"{path.suffix if path.stem == self._node.name else path.name}")
        except AttributeError:
            pass

    def save_json(self, filename, obj):
        self.save(filename, json.dumps(obj, indent=4))

    def load_json(self, filename):
        path = self.path() / filename
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
