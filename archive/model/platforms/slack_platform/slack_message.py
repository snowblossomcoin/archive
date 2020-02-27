from archive.model.message import Message
import re
import html
import logging
import mimetypes


def message_factory(users, channels, message: dict):
    message_type = message.get('type')
    message_subtype = message.get('subtype')

    if message_type == "message":
        if message_subtype == 'bot_message':
            return BotMessage(users, message, channels)
        elif message_subtype == 'file_comment':
            return FileComment(users, message, channels)
        elif message_subtype:
            # print(message)
            pass
    return SlackMessage(users, message, channels)


class SlackMessage(Message):
    username_regex = r'<@([^>]+)>'

    def __init__(self, users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = "slack_message"
        self.users = users

    def timestamp(self):
        return float(self.data['ts'])

    def __repr__(self):
        return self.data['ts']

    def _get_user_by_id(self, id):
        user = self.users.get(id)
        if not user:
            print(self.data)
            quit()
        return user

    def _get_user_ids_from_messsage(self):
        user_ids = re.findall(SlackMessage.username_regex, self.data['text'])
        return user_ids

    def username(self):
        user_id = self.data.get('user')
        user = self._get_user_by_id(user_id)
        profile = user.get('profile')
        name = profile.get('display_name_normalized') or profile.get('real_name_normalized')
        if not name:
            print(user)
            quit()
        return name

    def avatar(self):
        user_id = self.data.get('user')
        return user_id

    def text(self):
        text = self.data['text']

        if 'attachments' in self.data:
            for attachment in self.data['attachments']:
                if 'fallback' in attachment:
                    text += attachment['fallback']
                if 'title_link' in attachment:
                    text += attachment['title_link']

        # text = html.escape(text)
        # user_mention_regex = r'(&lt;@([^(?!&gt;)]+)&gt;)'

        user_mention_regex = r'(<@([^>]+)>)'
        matches = re.findall(user_mention_regex, text)
        unique_matches = set(matches)
        for match in unique_matches:
            mention, user_id = match
            try:
                user = self.users[user_id]
                name = user['profile']['display_name_normalized'] or user['profile']['real_name_normalized']
                resolved_mention = f'<span class="user_mention">@{ name }</span>'
                text = text.replace(mention, resolved_mention)
            except:
                logging.exception("")

        # resolve links <http(s)://>
        link_regex = r'<(https?: //[^ | >]+)>'
        text = re.sub(link_regex, r'<a target="_blank" href="\1">\1</a>', text)

        link_regex = r'<(https?://[^|>]+)\|?(.*)>'
        text = re.sub(link_regex, r'<a target="_blank" href="\1">\1</a>', text)

        return text

    def files(self):
        if 'files' in self.data:
            for file in self.data['files']:
                yield mimetypes.guess_extension(file['mimetype']), file


class BotMessage(SlackMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def avatar(self):
        return self.data['bot_id']

    def username(self):
        return self.data.get('username')


class FileComment(SlackMessage):

    def username(self):
        user_id = self._get_user_ids_from_messsage()[0]
        user = self._get_user_by_id(user_id)
        profile = user.get('profile')
        username = profile.get('display_name_normalized') or profile.get('real_name_normalized')
        return username
