from .capability import Capability, CapabilityDependencyException
from jinja2 import Environment, FileSystemLoader


class HtmlTemplate(Capability):
    def __init__(self, template_directory, template, save_as, *args, **kwargs):
        super(HtmlTemplate, self).__init__(*args, **kwargs)
        self._template = Environment(loader=FileSystemLoader(template_directory)).get_template(template)
        self._save_as = save_as
        self._node = None

    def update(self, node):
        self._node = node
        if not hasattr(self._node, "html_path"):
            raise CapabilityDependencyException("HtmlTemplate capability depends on FilePath with key 'html_path'")

    def get_mappings(self):
        return {"html_template": self}

    def render(self, context=None):
        context = context or {}
        context.update(node=self._node)
        html = self._template.render(**context)
        self._node.html_path.save(self._save_as, html)
