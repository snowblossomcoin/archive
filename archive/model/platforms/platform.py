import archive
from archive.common.graph import Node
from archive.common.graph.capabilities import Log, Config, FilePath, Path, HtmlTemplate, RecursiveMethod


class Platform(Node):
    def __init__(self, credentials, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_capabilities([Config()])
        self.add_capabilities([
            Log(),
            Path,
            FilePath(key="raw_path", is_file=False),
            FilePath(key="html_path", is_file=False),
            HtmlTemplate(template_directory=archive.web_path, template="base.html", save_as="index.html"),
            RecursiveMethod(key='fetch_all', method_name='fetch'),
            RecursiveMethod(key='render_all', method_name='render')
        ])
        self.credentials = credentials
