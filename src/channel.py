import json
import os

from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service():
        api_key: str = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        if channel_id == 'Новое название':
            raise AttributeError(self.__channel_id)



    @property
    def channel(self):
        youtube = Channel.g
        return youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.channel
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(self):
        api_key: str = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel(self):
        youtube = Channel.get_service()
        return youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

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

    def to_json(self):
        pass
