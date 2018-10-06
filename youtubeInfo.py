import requests
from bs4 import BeautifulSoup as bs
import json
import re
import validators
import logging

def __fetchAElemen(url):
    """ Fetch html from url and return all elements with a tag.

    Keyword arguments:
    url -- The url where to fetch the html.
    """

    response=requests.get(url)
    page = response.content

    soup = bs(page, features="html.parser")
    elementList = soup.find_all("a")
    return elementList


def __getvideoIds(elementList):
    """ Return urls for videos from elements.

    Keyword arguments:
    elementList -- List of bs4 element tags.
    """

    ids = []
    for video in elementList:
        try:
            if( 'pl-video-title-link' in video.attrs['class']):
                url = video['href']

                # Parsing video id from the url
                strings = re.split(r"[=&]", url)
                ids.append(strings[1])
        except:
            continue

    return ids


def __getVideoTitles(elementList):
    """ Return titles for videos from elements.

    Keyword arguments:
    elementList -- List of bs4 element tags.
    """

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
    """ Return creators for videos from elements.

    Keyword arguments:
    elementList -- List of bs4 element tags.
    """

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


def __buildVideoInfoList(videoIds, videoCreators, videoTitles):
    """ Return list containing video data in dictionaries.

    Keyword arguments:
    videoIds -- List of video ids.
    videoCreators -- List of video creators.
    videoTitles -- List of video titles.
    """

    # Check if lists are different lengths and return "Error" if so.
    if((len(videoIds) != len(videoCreators)) or
        (len(videoIds) != len(videoTitles)) or
        (len(videoIds) == 0)):
        logging.warning("Data fetched from playlist is not valid.")
        return []

    videoDictionaryList = []
    for index in range(len(videoIds)):
        item = {"id": videoIds[index].replace("b'", "'").replace("'", ""), "creator": videoCreators[index].replace("b'", "'").replace("'", ""), "name": videoTitles[index].replace("b'", "'").replace("'", "")}
        videoDictionaryList.append(item)

    return videoDictionaryList


def getPlaylistVideoinfo(url):
    """ Return list cotnaining video in dictionary from given playlist.

    Keyword arguments:
    url -- Url of the playlist.
    """

    if(not validators.url(url)):
        logging.error(f"Url {url} is not valid.")
        return []

    elements = __fetchAElemen(url)
    return __buildVideoInfoList(__getvideoIds(elements), __getVideoCreators(elements), __getVideoTitles(elements))