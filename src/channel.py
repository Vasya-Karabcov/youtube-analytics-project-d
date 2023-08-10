import json
import os

from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    # def print_info(self) -> None:
    #     """Выводит в консоль информацию о канале."""
    #     api_key: str = os.getenv('API_KEY')
    #     youtube = build('youtube', 'v3', developerKey=api_key)
    #     channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #     print(channel)
    #
    #
    #
    #     print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, json_file):
        info_channel = {'channel_id': self.__channel_id,
                        'title': self.title,
                        'description': self.description,
                        'url': self.url,
                        'subscriber_count': self.subscriber_count,
                        'video_count': self.video_count,
                        'view_count': self.view_count,
                        }
        with open(json_file, 'w') as outfile:
            json.dump(info_channel, outfile, indent=2, ensure_ascii=False,)
