from archive.model.channel import Channel
from datetime import datetime, timezone
from .slack_date import SlackDate


class SlackChannel(Channel):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def fetch(self, begin_anew=False):
        last_fetched_date = self.determine_last_fetched_date()
        if begin_anew or not last_fetched_date:
            oldest = 0
        else:
            oldest = int(datetime.strptime(last_fetched_date, "%Y-%m-%d").timestamp())

        for date, messages in self.parent.client.channel_history_by_date(self.data['id'], oldest=oldest):
            self.raw_path.save_json(f"{date}.json", messages)

    def render(self, begin_anew=False):
        dates = sorted(self.raw_path().glob("*-*-*.json"))
        for date in dates:
            self.add_children(SlackDate(parent=self, name=f"{date.stem}"))
        self.html_template.render()
