import requests


proxies = {
    'http': 'http://login:password@ip:port',
    'https': 'https://login:password@ip:port'
}

data = requests.get("https://ipinfo.io/json", proxies=proxies)
print(data.json())
