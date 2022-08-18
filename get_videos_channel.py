import json
from creds import *


def main():
    channelId = 'UC2YuAWMxh5oslkP6fb7-u6Q'

    data = get_service_simple('youtube', 'v3').search().list(
        channelId=channelId,
        part='snippet',
        type='video',
        order='date',
        maxResults='4'
    ).execute()
    print(json.dumps(data))


if __name__ == "__main__":
    main()