import json
from creds import *


def get_user_info():
    data = get_service_creds('oauth2', 'v2').userinfo().get().execute()
    print(json.dumps(data))


if __name__ == "__main__":
    get_user_info()