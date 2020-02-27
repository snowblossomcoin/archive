from archive.model.platforms.platform import Platform
from archive.model.platforms.slack_platform.slack_channel import SlackChannel
from archive.common.graph.capabilities import Log
from archive.model.platforms.slack_platform.slack_meta_client import SlackMetaClient
import shutil


class SlackPlatform(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "slack"
        self.client = SlackMetaClient(
            credentials=self.credentials,
            path=self.raw_path(),
            online=False,
            parent_logger=self.log
        )

    def fetch(self, *args, **kwargs):
        self.client.online = True
        self.client.users
        for channel in self.client.channels:
            self.add_children(SlackChannel(parent=self, name=channel, data=self.client.channels[channel]))

    def render(self, *args, **kwargs):
        self.client.online = False
        self.client.users
        for channel in self.client.channels:
            self.add_children(SlackChannel(parent=self, name=channel, data=self.client.channels[channel]))

        # copy avatars
        shutil.copytree(
            self.raw_path() / '_avatars',
            self.html_path() / '_avatars',
            # don't bother overwriting
            ignore=lambda path, files: [f for f in files if (self.html_path() / '_avatars' / f).is_file()],
            dirs_exist_ok=True
        )
        # copy files
        shutil.copytree(
            self.raw_path() / '_files',
            self.html_path() / '_files',
            # don't bother overwriting
            ignore=lambda path, files: [f for f in files if (self.html_path() / '_avatars' / f).is_file()],
            dirs_exist_ok=True
        )
        self.html_template.render()
