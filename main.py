import requests
from bs4 import BeautifulSoup as bs
url = "http://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v"

response=requests.get(url)
page = response.content

soup = bs(page, features="html.parser")
#videoList = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-playlist-video-renderer"})
videoList = soup.find_all("a")
links = []
for item in videoList:
    try:
        if( 'pl-video-title-link' in item.attrs['class']):
            print(item)
            links.append(item)
    except:
        continue

print(len(links))
'''
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        print(chunk)
'''

