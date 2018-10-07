# youtubeInfo

Module to fetch basic video info from youtube playlist.


## How to use

```
    import youtubeInfo as yt
    # Get playlist info.
    playlistUrl = "https://www.youtube.com/playlist?list=PL3zIYvF1XjLkK2zbqBtN-eYwxG-bH_yWs"
    videoList = yt.getPlaylistVideoInfo(playlistUrl)
    print(videoList)
    ''' Content of videoList will be like: 
      [
        {'id': 'kulPdl27Ubc', 'creator': 'TechLinked', 'name': 'b"WERE BACK BABY!!!"'},
        {'id': '6yV1JUmlqgc', 'creator': 'TechLinked', 'name': 'Valve makes new Fortnite competitor'},
        ...
      ]
    '''
    
    # Get video info.
    videoUrl = "https://www.youtube.com/watch?v=JdEijZ9XJmM&t=0s"
    videoInfo = yt.getVideoInfo(videoUrl)
    print(videoInfo)
    ''' Content of videoInfo will be like: 
      {'video_id': 'JdEijZ9XJmM', 'author': 'Derek Banas', 'title': 'Arduino 9 : Arduino Pong', 'length_seconds': '1718'}
    '''
```
