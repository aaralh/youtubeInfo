import requests
from bs4 import BeautifulSoup as bs
import json

url = "http://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v"

response=requests.get(url)
page = response.content

soup = bs(page, features="html.parser")
videoList = soup.find_all("a")
creatorList = soup.find_all("a")
links = []
videoNames = []
creators = []


for video in videoList:
    try:
        if( 'pl-video-title-link' in video.attrs['class']):
            links.append(video['href'])
            
    except:
        continue


for creator in creatorList:
    try:
        if( 'yt-uix-sessionlink' in creator.attrs['class'] and 'spf-link' in creator.attrs['class']):
            if(('dir' in creator.attrs) == False):
                creators.append(str(creator.contents[0]))
            if(('data-title' in creator.attrs) == False):
                line = creator.contents[0].replace('\n', '')
                line = line.strip()
                videoNames.append(str(line))
    except:
        continue


videoDictionaryList = []

for index in range(len(links) - 1):
    item = str({"url": links[index].decode("utf-8"), "creator": creators[(26 + index)].decode("utf-8"), "name": videoNames[index].decode("utf-8")})
    videoDictionaryList.append((str(item.decode("utf-8"))))

print(videoDictionaryList)