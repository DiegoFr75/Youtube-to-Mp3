# Youtube to Mp3
A python script to download and convert videos from youtube to mp3

## Description

This script will download the video from youtube using the pytube library, soon after, it will convert to mp3 using ffmpeg, and finally will delete the video, leaving only the audio in mp3 192 kbps.

## Requirements
- Python 3+
- FFmpeg
- Pytube library (https://github.com/nficano/pytube)

<b>Note:</b> In order for you to perform the conversion it is necessary to have ffmpeg installed and added to your environment variables.  
You can find it here: https://ffmpeg.zeranoe.com/builds/

## Command-line interface
- -u to specify the youtube url
- -p to specify the path where the file(s) will be saved

To download a video or a playlist.<br>
<b>Note:</b> The file(s) will be saved in the same directory of YoutubeToMp3.py file.
```bash
# python YoutubeToMp3.py -u youtube_url
python YoutubeToMp3.py -u https://www.youtube.com/watch?v=luwVgiNH7HU
```
To specify a path.<br>
<b>Note:</b> The order of path and url does not matter, but, the url must always be informed. 
```bash
# python YoutubeToMp3.py -p path -u youtube_url
python YoutubeToMp3.py -p C:\Users\randomUser\Download -u https://www.youtube.com/playlist?list=PLrX1cR5KH3pqpCqDmcyLskDUYRtALPhwG
```
<b>Note:</b> Remember to use "" if your directory have spaces.



