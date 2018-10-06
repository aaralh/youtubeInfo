import requests
from bs4 import BeautifulSoup as bs
import json

def __fetchAElemen(url):
    '''
    Fetches the html from given url and retruns all elements found with a tag.
    '''
    response=requests.get(url)
    page = response.content

    soup = bs(page, features="html.parser")
    elementList = soup.find_all("a")
    return elementList


def __getVideoUrls(elementList):
    '''
    Returns urls for videos from elements.
    '''
    links = []
    for video in elementList:
        try:
            if( 'pl-video-title-link' in video.attrs['class']):
                links.append(video['href'])      
        except:
            continue

    return links


def __getVideoTitles(elementList):
    '''
    Returns titles for videos from elements.
    '''
    titles = []
    for video in elementList:
        try:
            if( 'yt-uix-sessionlink' in video.attrs['class'] and
                    'spf-link' in video.attrs['class'] and
                    'dir' in video.attrs):
                content = video.contents[0].replace('\n', '')
                content = content.strip()
                if(content != ""):
                    titles.append(str(content.encode("utf-8")))
        except:
            continue
    if(len(titles) > 1):
        titles = titles[1:]

    return titles

def __getVideoCreators(elementList):
    '''
    Returns creators for videos from elements.
    '''
    creators = []
    for video in elementList:
        try:
            if( 'yt-uix-sessionlink' in video.attrs['class'] and
                    'spf-link' in video.attrs['class'] and
                    ('dir' in video.attrs) == False):
                content = video.contents[0].replace('\n', '')
                content = content.strip()
                if(content != ""):
                    creators.append(str(content.encode("utf-8")))
        except:
            continue

    if(len(creators) > 2):
        creators = creators[2:]
    
    return creators


def __buildJson(videoUrls, videoCreators, videoTitles):
    '''
    Returns json built from fetched data.
    '''
    videoDictionaryList = []

    for index in range(len(videoUrls) - 1):
        item = {"url": videoUrls[index].replace("b'", "'").replace("'", ""), "creator": videoCreators[index].replace("b'", "'").replace("'", ""), "name": videoTitles[index].replace("b'", "'").replace("'", "")}
        videoDictionaryList.append(item)

    return json.dumps(str(videoDictionaryList))


def getPlaylistVideoinfo(url):
    elements = __fetchAElemen(url)
    creators = __getVideoCreators(elements)
    titles = __getVideoTitles(elements)
    urls = __getVideoUrls(elements)
    return __buildJson(urls, creators, titles)