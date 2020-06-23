from archive.model.platforms.platform import Platform
from archive.model.platforms.slack_platform.slack_channel import SlackChannel
from archive.common.graph.capabilities import Log
from archive.model.platforms.slack_platform.slack_meta_client import SlackMetaClient
import os
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


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
        #shutil.copytree(
        copytree(
            self.raw_path() / '_avatars',
            self.html_path() / '_avatars',
            ignore=lambda path, files: [f for f in files if (self.html_path() / '_avatars' / f).is_file()],
        )
        # copy files
        #shutil.copytree(
        copytree(
            self.raw_path() / '_files',
            self.html_path() / '_files',
            ignore=lambda path, files: [f for f in files if (self.html_path() / '_avatars' / f).is_file()],
        )
        self.html_template.render()
