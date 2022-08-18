from creds import *


def get_channel_info(channel_id):
    data = get_service_simple("youtube", "v3").channels().list(id=channel_id, part='snippet, statistics').execute()
    
    nameChannel = data['items'][0]['snippet']['title']
    descriptionChannel = data['items'][0]['snippet']['description']
    createdAt = data['items'][0]['snippet']['publishedAt']
    viewCount = data['items'][0]['statistics']['viewCount']
    subscriberCount = data['items'][0]['statistics']['subscriberCount']
    videoCount = data['items'][0]['statistics']['videoCount']

    print(f'Название - {nameChannel}')
    print(f'Описание - {descriptionChannel}')
    print(f'Дата создания - {createdAt}')
    print(f'Количество просмотров - {viewCount}')
    print(f'Количество подписчиков - {subscriberCount}')
    print(f'Количество видео - {videoCount}')


def get_video_info(video_id):
    data = get_service_simple("youtube", "v3").videos().list(id=video_id, part='snippet, statistics').execute()

    nameVideo = data['items'][0]['snippet']['title']
    descriptionVideo = data['items'][0]['snippet']['description']
    publishedAt = data['items'][0]['snippet']['publishedAt']
    viewCount = data['items'][0]['statistics']['viewCount']
    likeCount = data['items'][0]['statistics']['likeCount']
    commentCount = data['items'][0]['statistics']['commentCount']

    print(f'Название - {nameVideo}')
    print(f'Описание - {descriptionVideo}')
    print(f'Дата публикации - {publishedAt}')
    print(f'Количество просмотров - {viewCount}')
    print(f'Количество лайков - {likeCount}')
    print(f'Количество комментариев - {commentCount}')


def main():
    get_channel_info(channel_id='UCGte1pK_uDl4XkFAh1bWXBg')
    get_video_info(video_id='04y6usZ9sxY')


if __name__ == "__main__":
    main()