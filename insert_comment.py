import json
from creds import *


def main():
    channelId = 'UCGte1pK_uDl4XkFAh1bWXBg'
    videoId = '04y6usZ9sxY'
    comment = 'тестовый комментарий'

    data = get_service_creds('youtube', 'v3').commentThreads().insert(
        part = "snippet",
        body = dict(
            snippet = dict(
                channelId = channelId,
                videoId = videoId,
                topLevelComment = dict(
                    snippet = dict(
                        textOriginal = comment
                    )
                )
            )
        )
    ).execute()
    print(json.dumps(data))


if __name__ == "__main__":
    main()