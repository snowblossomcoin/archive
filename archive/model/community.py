import archive
from archive.common.graph import Node
from archive.common.graph.capabilities import Log, Config, FilePath, Path, HtmlTemplate, RecursiveMethod
from archive.model.platforms import supported_platforms


class Community(Node):
    def __init__(self, platforms, *args, **kwargs):
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
        for platform in platforms:
            platform_name = platform['name']
            platform_class = supported_platforms[platform_name]
            platform_obj = platform_class(parent=self, credentials=platform['credentials'])
            self.add_children(platform_obj)

    def render(self, *args, **kwargs):
        self.html_path.copy(archive.web_path / 'style.css')
        self.html_template.render()
