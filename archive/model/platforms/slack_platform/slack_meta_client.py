from ..platform_meta_client import PlatformMetaClient
import json
from datetime import datetime, timezone
import time
import requests
from slack import WebClient
import mimetypes
import pprint


class SlackMetaClient(PlatformMetaClient):
    def __init__(self, *args, **kwargs):
        super(SlackMetaClient, self).__init__(*args, **kwargs)
        self.client = WebClient(**self.credentials)
        self.__users = dict()
        self.__channels = dict()
        self.path.mkdir(parents=True, exist_ok=True)

    def _fetch_avatar(self, user):
        self.log.debug(f"_fetch_avatar, {user['id']}")

        try:
            profile = user['profile']
        except:
            profile = user['icons']

        avatar_path = self.path / "_avatars"
        avatar_path.mkdir(parents=True, exist_ok=True)
        save_as = avatar_path / f"{user['id']}.png"
        if not save_as.is_file():
            for attempt in range(3):
                try:
                    r = requests.get(
                        profile.get('image_72') or profile.get('image_64') or profile.get('image_48'),
                        # headers={"Authorization": f"Bearer {self.credentials['token']}"} # nope
                    )
                    r.raise_for_status()
                    with open(save_as, 'wb') as f:
                        f.write(r.content)
                    time.sleep(1)
                    break
                except requests.HTTPError:
                    self.log.exception(pprint.pprint(user))
                    time.sleep(10)

    def _fetch_file(self, file):
        self.log.debug(f"_fetch_file, {file['id']}")

        file_path = self.path / "_files"
        file_path.mkdir(parents=True, exist_ok=True)

        extension = mimetypes.guess_extension(file['mimetype'])
        filename = file_path /  f"{file['id']}{extension}"
        if not filename.is_file():
            r = requests.get(
                file['url_private_download'],
                headers={"Authorization": f"Bearer {self.credentials['token']}"}
            )
            with open(filename, 'wb+') as f:
                f.write(r.content)
            time.sleep(1)

        if 'thumb_64' in file:
            filename = file_path / f"{file['id']}_thumb_64.png"
            if not filename.is_file():
                r = requests.get(
                    file['thumb_64'],
                    headers={"Authorization": f"Bearer {self.credentials['token']}"}
                )
                with open(filename, 'wb+') as f:
                    f.write(r.content)
                time.sleep(1)

    @property
    def users(self):
        if not self.__users:
            try:
                with open(self.path / 'users.json', 'r') as f:
                    for user in json.load(f):
                        self.__users.update({user['id']: user})
            except FileNotFoundError:
                pass

            if self.online:
                for page in self.client.users_list():
                    for user in page['members']:
                        if not user['id'] in self.__users:
                            self._fetch_avatar(user)
                        self.__users.update({user['id']: user})

                with open(self.path / 'users.json', 'w') as f:
                    json.dump(list(self.__users.values()), f, indent=4)

        return self.__users

    @users.setter
    def users(self, user):
        self._fetch_avatar(user)
        self.__users.update({user['id']: user})
        with open(self.path / 'users.json', 'w') as f:
            json.dump(list(self.__users.values()), f, indent=4)

    @property
    def channels(self):
        if not self.__channels:
            try:
                with open(self.path / 'channels.json', 'r') as f:
                    for channel in json.load(f):
                        self.__channels.update({channel['name_normalized']: channel})
            except FileNotFoundError:
                pass

            if self.online:
                for page in self.client.channels_list():
                    for channel in page['channels']:
                        self.__channels.update({channel['name_normalized']: channel})

            with open(self.path / 'channels.json', 'w') as f:
                json.dump(list(self.__channels.values()), f, indent=4)

        return self.__channels

    def channel_history(
        self,
        channel_id,
        oldest=0,
        latest=int(datetime.now().timestamp())
    ):
        cursor = latest
        while True:
            page = self.client.channels_history(
                channel=channel_id,
                oldest=oldest,
                latest=cursor,
                count=1000
            )
            for message in page['messages']:
                cursor = int(float(message['ts']))
                yield message

                if 'bot_id' in message and not message['bot_id'] in self.__users:
                    self.users = self.client.bots_info(bot=message['bot_id'])['bot']
                    time.sleep(1)

                if 'files' in message:
                    for file in message['files']:
                        if 'url_private_download' in file:
                            self._fetch_file(file)

            if not page['has_more']:
                break

    def channel_history_by_date(
        self,
        channel_id,
        oldest=0,
        latest=int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    ):

        last_message_date = datetime.fromtimestamp(latest, tz=timezone.utc).date()
        message_date = last_message_date
        messages = []

        for message in self.channel_history(
            channel_id,
            oldest,
            latest
        ):
            message_date = datetime.fromtimestamp(float(message['ts']), tz=timezone.utc).date()
            if message_date != last_message_date:
                if messages:
                    yield last_message_date, messages[::-1]
                last_message_date = message_date
                messages = []
            messages.append(message)

        if messages:
            yield message_date, messages[::-1]
