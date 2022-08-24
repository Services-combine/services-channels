import time
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


automatic_youtube = AutomaticYoutube()
automatic_youtube.start()
