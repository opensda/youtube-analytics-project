import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Данные плейлиста в соответствии с его id

        self.playlist = self.youtube.playlists().list(id=playlist_id,
                                             part='snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

        # Данные о всех видео плейлиста в соответствии с его id

        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        # Неспосредственно статистика по всем видео плейлиста

        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()




    def __str__(self):
        return f'{self.title}, {self.url}'

    @property
    def total_duration(self):
        """
        Считает продолжительность всех видео плейлиста
        """

        # Список, куда складываем объекты datetime
        durations = []
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations.append(duration)

            # Вычисляем суммарную продолжительность всех видео плейлиста

        sum_datetime = sum(durations, datetime.timedelta())
        return sum_datetime

    def show_best_video(self):
        """
        Показывает ссылку на видео с наибольшим количеством лайков
        """

        # Извлекаем из статистики только лайки


        likes_store = []
        for data in self.video_response['items']:
            likes_store.append(data['statistics']['likeCount'])

         # Преобразовываем лайки в числа

        likes_store_int = []
        for like in likes_store:
            likes_store_int.append(int(like))

        # Находим id видео с наибольшим количеством лайков

        for x in self.video_response['items']:
            if x['statistics']['likeCount'] == str(max(likes_store_int)):
                video_id = x['id']

        # Получаем ссылку на видео

        best_video = f"https://youtu.be/{video_id}"
        return best_video








