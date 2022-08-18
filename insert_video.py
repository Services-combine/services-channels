from random import randrange
from time import sleep
from googleapiclient.http import MediaFileUpload
from creds import *


def video_upload(video_path, title, description, status):
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    meta = {
        'snippet': {
            'title' : title,
            'description' : description
        },
        'status':{
            'privacyStatus': status
        }
    }

    insert_request = get_service_creds("youtube", "v3").videos().insert(
        part=','.join(meta.keys()),
        body=meta,
        media_body=media
    )

    r = resumable_upload(insert_request)
    print(r)


def resumable_upload(request, retries=5):
    while retries > 0:
        try:
            status, response = request.next_chunk()

            if response is None: continue
            if 'id' not in response: 
                raise Exception("no id found while video uploading")

            return response
        except Exception as e:
            print(e)
            retries -= 1
            sleep(randrange(5))

    return None


def main():
    video_upload(
        video_path='3.mp4', 
        title="Как рычит белочка",
        description="Описание видео, где рычит белочка",
        status="private"
    )


if __name__ == "__main__":
    main()