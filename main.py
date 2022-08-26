import time
import json
import requests
from math import ceil
from database import Database
from creds import *
from config import *


class AutomaticYoutube:   

    def __init__(self):
        try:
            self.db = Database() 
            logger.info("Success connect to MongoDB")
        except Exception as error:
            logger.error(error)


    def get_uploads_playlist_id_proxy(self, channel_id, api_key):
        try:
            url = 'https://youtube.googleapis.com/youtube/v3/channels'
            params = {
                'part' : 'contentDetails',
                'id': channel_id,
                'key': api_key
            }
            headers={
                "Accept": "application/json"
            }

            response = requests.get(url, params=params, headers=headers).json()

            if response.get('error'):
                logger.error(f"channel_id: {channel_id}: {response['error']['message']}")
                return None
            else:
                uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            logger.info(f"Success get uploads playlist id {channel_id}")
            return uploads_playlist_id
        except Exception as error:
            logger.error(error)
            return None


    def get_videos_channel_proxy(self, channel_id, api_key, count_videos, access_token):
        try:
            videos = []
            uploads_playlist_id = self.get_uploads_playlist_id_proxy(channel_id, api_key)
            if uploads_playlist_id == None:
                return []

            maxResults = 50
            url = 'https://youtube.googleapis.com/youtube/v3/playlistItems'
            params = {
                'playlistId' : uploads_playlist_id,
                'part' : 'snippet',
                'maxResults': maxResults,
            }
            headers = {
                "Accept": "application/json",
                "Authorization": f'Bearer {access_token}'
            }

            for _ in range(ceil(count_videos / maxResults)):
                response = requests.get(url, params=params, headers=headers).json()

                if response.get('error'):
                    logger.error(f"channel_id: {channel_id}: {response['error']['message']}")
                    return []
                else:
                    for item in response['items']:
                        videos.append(item['snippet']['resourceId'].get('videoId'))

                    params['pageToken'] = response.get('nextPageToken')
                    if not params['pageToken']: break

            logger.info(f"Success get videos {channel_id}")
            return videos
        except Exception as error:
            logger.error(error)
            return []


    def commenting_videos_proxy(self, channel):
        try:
            channel_id = channel['channelid']
            api_key = channel['apikey']
            count_videos = channel['countcommentedvideos']
            comment = channel['comment']
            #user_token = f'{FOLDER_CHANNELS}user_token_{channel_id}.json'
            user_token = 'user_token.json'

            service = get_service_creds(user_token, 'youtube', 'v3')
            with open(user_token, 'r') as file:
                user_token_data = json.load(file)

            videos = self.get_videos_channel_proxy(channel_id, api_key, count_videos, user_token_data['token'])
            videos = videos[:count_videos]

            url = 'https://youtube.googleapis.com/youtube/v3/commentThreads'
            params = {
                'part' : 'snippet',
                'key': api_key
            }
            headers={
                "Authorization": f"Bearer {user_token_data['token']}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            for videoId in videos:
                try:
                    request = service.commentThreads().insert(
                        part = "snippet",
                        body = dict(
                            snippet = dict(
                                channelId = channel_id,
                                videoId = videoId,
                                topLevelComment = dict(
                                    snippet = dict(
                                        textOriginal = comment
                                    )
                                )
                            )
                        )
                    ).to_json()

                    request_json = json.loads(request)
                    response = requests.post(url, params=params, headers=headers, data=request_json['body']).json()

                    if response.get('error'):
                        logger.error(f"video_id: {videoId} channel_id: {channel_id}: {response['error']['message']}")
                    else:
                        logger.info(f'Commented is success video_id: {videoId} channel_id: {channel_id}')

                    if videoId != videos[-1]:
                        time.sleep(15)

                except Exception as error:
                    logger.error(error)

            logger.info(f'Commenting on the channel {channel_id} has been successfully completed')
        except Exception as error:
            logger.error(error)


    def get_uploads_playlist_id(self, service, channel_id):
        try:
            data = service.channels().list(id=channel_id, part='contentDetails').execute()
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            logger.info(f"Success get uploads playlist id {channel_id}")
            return uploads_playlist_id
        except Exception as error:
            logger.error(error)
            return None


    def get_videos_channel(self, channel_id, api_key, count_videos):
        try:
            service = get_service_simple(api_key)
            videos = []
            uploads_playlist_id = self.get_uploads_playlist_id(service, channel_id)
            if uploads_playlist_id == None:
                return []

            maxResults = 50
            args = {
                'playlistId' : uploads_playlist_id,
                'part' : 'snippet',
                'maxResults': maxResults,
            }

            for _ in range(ceil(count_videos / maxResults)):
                data = service.playlistItems().list(**args).execute()
                for item in data['items']:
                    videos.append(item['snippet']['resourceId'].get('videoId'))

                args['pageToken'] = data.get('nextPageToken')
                if not args['pageToken']: break

            logger.info(f"Success get videos {channel_id}")
            return videos
        except Exception as error:
            logger.error(error)
            return []


    def commenting_videos(self, channel):
        try:
            channel_id = channel['channelid']
            api_key = channel['apikey']
            count_videos = channel['countcommentedvideos']
            comment = channel['comment']
            user_token = f'{FOLDER_CHANNELS}user_token_{channel_id}.json'

            videos = self.get_videos_channel(channel_id, api_key, count_videos)
            videos = videos[:count_videos]
            service = get_service_creds(user_token, 'youtube', 'v3')

            for videoId in videos:
                try:
                    service.commentThreads().insert(
                        part = "snippet",
                        body = dict(
                            snippet = dict(
                                channelId = channel_id,
                                videoId = videoId,
                                topLevelComment = dict(
                                    snippet = dict(
                                        textOriginal = comment
                                    )
                                )
                            )
                        )
                    ).execute()
                    logger.info(f'Commented is success video_id: {videoId} channel_id: {channel_id}')

                    if videoId != videos[-1]:
                        time.sleep(15)
                        
                except Exception as error:
                    logger.error(error)

            logger.info(f'Commenting on the channel {channel_id} has been successfully completed')
        except Exception as error:
            logger.error(error)


    def start(self):
        try:
            while True:
                channel = self.db.get_channel_launch()

                if channel != None:
                    self.commenting_videos(channel)
                    self.db.suspend_channel(channel['_id'])
                    logger.info(f'Change status launch {channel["channelid"]}')

                time.sleep(15)
        except Exception as error:
            logger.error(error)


    def start_proxy(self):
        try:
            while True:
                channel = self.db.get_channel_launch()

                if channel != None:
                    self.commenting_videos_proxy(channel)
                    self.db.suspend_channel(channel['_id'])
                    logger.info(f'Change status launch {channel["channelid"]}')

                time.sleep(15)
        except Exception as error:
            logger.error(error)


automatic_youtube = AutomaticYoutube()
#automatic_youtube.start()
automatic_youtube.start_proxy()