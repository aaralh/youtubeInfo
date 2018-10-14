import requests
import re
import validators
import logging
import time
from bs4 import BeautifulSoup as bs

def __fetchVideoInfo(url):
    """ Fetch video info from url and return json.

    Keyword arguments:
    url -- The url where to fetch the html.
    """

    response = requests.get(url)

    strings = re.split('<[^>]*script', str(response.content))
    return strings[33]


def __fetchAElement(url):
    """ Fetch html from url and return all elements with a tag.

    Keyword arguments:
    url -- The url where to fetch the html.
    """

    response = requests.get(url)
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
        item = {"id": videoIds[index].replace("b'", "'").replace("'", ""),
                "creator": videoCreators[index].replace("b'", "'").replace("'", ""),
                "name": videoTitles[index].replace("b'", "'").replace("'", "")}
        videoDictionaryList.append(item)

    return videoDictionaryList


def getPlaylistVideoInfo(url):
    """ Return list containing video in dictionary from given playlist.

    Keyword arguments:
    url -- Url of the playlist.
    """

    if(not validators.url(url)):
        logging.error(f"Url {url} is not valid.")
        return []

    elements = __fetchAElement(url)
    return __buildVideoInfoList(__getvideoIds(elements), __getVideoCreators(elements), __getVideoTitles(elements))


def getVideoInfo(url, ):
    """ Return dictionary containing video info.

    Keyword arguments:
    url -- Url of the video.
    """

    item = {}
    properties = ["video_id", "author", "title", "length_seconds"]
    element = __fetchVideoInfo(url)
    strings = re.split(r"[,\"]", str(element))
    error = False
    for prop in properties:
        try:
            item[prop] = str(strings[strings.index(prop) + 2].replace("\\", "").encode('ascii', 'ignore')).replace("b'", "'").replace("'", "")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            error = True
            continue

    if(error):
       logging.error("Error occure while getting video info")

    return item
