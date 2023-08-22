from datetime import timedelta

import isodate

from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        youtube = Channel.get_service()

        playlists = youtube.playlists().list(part="snippet", id=playlist_id).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        total_duration = timedelta()
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        max_likes = 0
        best_video_url = ''

        for video in video_response['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video_url = f'https://youtu.be/{video["id"]}'

        return best_video_url
