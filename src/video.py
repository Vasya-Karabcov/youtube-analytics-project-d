from src.channel import Channel


class YouTubeError(Exception):

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Нет такого id'

    def __str__(self):
        return self.message


class Video:

    def __init__(self, video_id):
        self.video_id = video_id

        youtube = Channel.get_service()

        video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                      id=video_id
                                      ).execute()

        try:
            self.title = video['items'][0]['snippet']['title']
            self.url_video = f'https://youtu.be/{self.video_id}'
            self.view_count = video['items'][0]['statistics']['viewCount']
            self.like_count = video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None


    def __str__(self):
        return f'{self.title}'



class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
