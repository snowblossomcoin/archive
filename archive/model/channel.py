import archive
from archive.common.graph import Node
from archive.common.graph.capabilities import Log, Config, FilePath, Path, HtmlTemplate, RecursiveMethod
from archive.model.date import Date


class Channel(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_capabilities([Config()])
        self.add_capabilities([
            Log(),
            Path,
            FilePath(key="raw_path", is_file=False),
            FilePath(key="html_path", is_file=False),
            HtmlTemplate(template_directory=archive.web_path, template='channel.html', save_as='index.html'),
            RecursiveMethod(key='fetch_all', method_name='fetch'),
            RecursiveMethod(key='render_all', method_name='render')
        ])

    def determine_last_fetched_date(self):
        fetched_dates = self.raw_path.path().glob("*-*-*.json")
        fetched_dates = set(map(lambda a: a.stem, fetched_dates))
        if fetched_dates:
            last_fetched_date = sorted(fetched_dates)[-1]
            return last_fetched_date
        return None

    def render(self, begin_anew=False):
        fetched_dates = set(map(lambda date: date.stem, self.raw_path().glob("*-*-*.json")))
        rendered_dates = list(sorted(map(lambda date: date.stem, self.html_path().glob("*-*-*.html"))))

        if begin_anew:
            unrendered_dates = fetched_dates
        else:
            unrendered_dates = fetched_dates.difference(set(rendered_dates))

        # make sure we re-render the last rendered date, to update the "next" link
        if rendered_dates:
            unrendered_dates.add(rendered_dates[:-1])

        unrendered_dates = sorted(unrendered_dates)

        for date in unrendered_dates:
            self.add_children(Date(parent=self, name=f"{date.stem}"))
        self.html_template.render()
