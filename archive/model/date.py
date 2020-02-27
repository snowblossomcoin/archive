import archive
from archive.common.graph import Node
from archive.common.graph.capabilities import Log, Config, FilePath, Path, HtmlTemplate, RecursiveMethod


class Date(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_capabilities([Config()])
        self.add_capabilities([
            Log(),
            Path,
            FilePath(key="raw_path", is_file=True),
            FilePath(key="html_path", is_file=True),
            HtmlTemplate(template_directory=archive.web_path, template="date.html", save_as=f"{self.name}.html"),
            RecursiveMethod(key='render_all', method_name='render')
        ])

    def render_context(self):
        messages = self.parent.raw_path.load_json(f"{self.name}.json")
        date_index = self.parent.children.index(self)
        dates = self.parent.children
        prev_href = f"{dates[date_index - 1]}.html" if date_index > 0 else ""
        next_href = f"{dates[date_index + 1]}.html" if date_index < len(dates) - 1 else ""
        context = {
            "prev_href": prev_href,
            "next_href": next_href,
            "messages": messages
        }
        return context

    def render(self, begin_anew=False, *args, **kwargs):
        if (self.parent.html_path() / f"{self.name}.html").is_file() or begin_anew:
            self.html_template.render(context=self.render_context())
