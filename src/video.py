import os
from googleapiclient.discovery import build

class Video:
    def __init__(self, video_id) -> None:

        # Создаем специальный объект для работы с YouTube

        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Статистика видео в соответствии с его id
        # Если id не существует, все остальные свойства None

        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def __str__(self):
        return f'{self.title}'



class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.title}'



