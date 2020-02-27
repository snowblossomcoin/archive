import archive
from archive.common.graph import Node
from archive.common.graph.capabilities import Log, Config, FilePath, Path, HtmlTemplate, RecursiveMethod
from archive.model.community import Community


class Archive(Node):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_capabilities([Config(config=config)])
        self.add_capabilities([
            Log(),
            Path,
            FilePath(key="raw_path", base_path=self.config['raw_path'], is_file=False),
            FilePath(key="html_path", base_path=self.config['html_path'], is_file=False),
            HtmlTemplate(template_directory=archive.web_path, template="base.html", save_as="index.html"),
            RecursiveMethod(key='fetch_all', method_name='fetch'),
            RecursiveMethod(key='render_all', method_name='render')
        ])
        for community in self.config['communities']:
            self.add_children(Community(parent=self, name=community['name'], platforms=community['platforms']))

    def fetch(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        self.html_path.copy(archive.web_path / 'style.css')
        self.html_template.render()
