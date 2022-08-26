import requests

# https://docs.microsoft.com/ru-ru/azure/developer/python/sdk/azure-sdk-configure-proxy?tabs=cmd

'''
proxies = { 'https' : 'https://user:password@proxyip:port' } 
r = requests.get('https://url', proxies=proxies) 
'''

proxies = {
    'https': 'https://ip:port'
}

data = requests.get("https://ipinfo.io/json", proxies=proxies)
print(data.text)
