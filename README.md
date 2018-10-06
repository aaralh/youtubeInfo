# youtubeInfo

Module to fetch basic video info from youtube playlist.

## How to use

```
    import youtubeInfo as yt
    url = "https://www.youtube.com/playlist?list=PL3zIYvF1XjLkK2zbqBtN-eYwxG-bH_yWs"
    videoList = yt.getPlaylistVideoinfo(url)
    print(videoList)
    ''' Contents of videoList will be like: 
      [
        {'id': 'kulPdl27Ubc', 'creator': 'TechLinked', 'name': 'b"WERE BACK BABY!!!"'},
        {'id': '6yV1JUmlqgc', 'creator': 'TechLinked', 'name': 'Valve makes new Fortnite competitor'},
        ...
      ]
    '''
```
