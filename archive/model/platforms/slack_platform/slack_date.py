from archive.model.date import Date
from . import slack_message


class SlackDate(Date):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_context(self):
        users = self.parent.parent.client.users
        channels = self.parent.parent.client.channels
        messages = [
            slack_message.message_factory(users, channels, data)
            for data in self.parent.raw_path.load_json(f"{self.name}.json")
        ]
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
        if not (self.parent.html_path.path() / f"{self.name}.html").is_file() or begin_anew:
            self.html_template.render(context=self.render_context())
