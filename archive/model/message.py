from datetime import datetime


class Message:
    def __init__(self, data: dict, *args, **kwargs):
        self.data = data
        self.template_name = "message"

    def timestamp(self):
        return "0"

    def human_datetime(self):
        ts = float(self.timestamp())
        return datetime.utcfromtimestamp(ts).isoformat(sep=" ", timespec="seconds")

    def avatar(self):
        return ""

    def username(self):
        return ""

    def text(self):
        return []
