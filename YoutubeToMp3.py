from pytube import YouTube
from pytube import Playlist
import os
import sys


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def percent(current, total):
    perc = 100 - (((float(current) / float(total)) * float(100)))
    return perc

class YoutubeToMp3:
    def __init__(self, youtube_url, path = None):
        if (path == "") or (path == None):
            self.path = os.path.abspath(__file__).replace(os.path.basename(__file__),"")
        else:
            if os.path.isdir(path):
                self.path = path + "\\"
            else:
                self.path = "invalid path"
                print("Invalid path")
            
        self.url = youtube_url
        self.type = self.defineUrlType()
        
        if(self.type == "invalid type" or self.path == "invalid path"):
            pass
        else:
            self.progress = 0
            self.playlist_progress = 0 
            error = False

            if (self.type == 'video'):
                try:
                    self.yt = YouTube(self.url, on_progress_callback=self.showProgressBar, on_complete_callback=self.showComplete)
                except:
                    print("An error has occurred")
                    error = True

                if not(error):
                    self.playlist_size = 1
                    self.download()
            else:
                try:
                    self.pl = Playlist(self.url)
                except:
                    print("An error has occurred")
                    error = True

                if not(error):
                    self.urls_playlist = self.pl.parse_links()
                    self.playlist_size = len(self.urls_playlist)
                    self.errors_playlist = 0         
                    self.playlistDownload()      

    def download(self):
        stream = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        self.itag = str(stream.itag)
        self.file_size = stream.filesize
        if not(self.checkFileExistence(stream.default_filename)):
            self.yt.streams.get_by_itag(self.itag).download(output_path = self.path)
        else:
            self.playlist_progress+=1
            print("\r"+"100% downloaded (" + str(self.playlist_progress) + "/" + str(self.playlist_size) + ")    ", end='')

    def playlistDownload(self):
        error = False
        for url in self.urls_playlist:
            try:
                self.yt = YouTube(url, on_progress_callback=self.showProgressBar,
                                        on_complete_callback=self.showComplete)
            except:
                error = True
                self.errors_playlist+=1
                pass

            if not(error):
                self.download()
            else:
                error = False

    def convertToMp3(self, stream):
        video_filename = stream.default_filename
        audio_filename = video_filename.replace(".mp4", ".mp3")
        to_mp3 = "ffmpeg -loglevel panic -i \"" + self.path + video_filename + "\" -f mp3 -ab 192000 -vn \"" + self.path + audio_filename + "\""
        os.system(to_mp3)
        os.remove(self.path + video_filename)
    
    def checkFileExistence(self, filename):
        file_name_mp3 = filename.replace('.mp4','.mp3')
        exists = os.path.isfile(file_name_mp3)

        return True if exists else False

    def defineUrlType(self):
        if self.url.find("watch?v=") != -1 :
            return "video"
        elif self.url.find("playlist?list=") != -1:
            return "playlist"

        return "invalid type"
    
    def showProgressBar(self, stream, chunk, file_handle, bytes_remaining):
        self.progress = int(percent(bytes_remaining, self.file_size))
        print("\r"+str(self.progress)+"% downloaded (" + str(self.playlist_progress) + "/" + str(self.playlist_size) + ")    ", end='')
                
    def showComplete(self, stream, file_hadle):
        if self.type == "video":
            print("\r"+"Download completed     \nConverting...", end='')
            self.progress = 0
            self.convertToMp3(stream)
            print("Done")
        else:
            self.playlist_progress+=1

            print("\nconverting...", end='')
            self.convertToMp3(stream)
            print("Done",end='')
            
            sys.stdout.write(ERASE_LINE)
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.flush()

            if (self.playlist_size - self.errors_playlist) == self.playlist_progress:
                print("\r"+str(self.progress)+"% downloaded (" + str(self.playlist_progress) + "/" + str(self.playlist_size) + ")    ", end='')
                self.progress = 0


if __name__=="__main__":
    #                0             1  2    3  4       
    #python ytPlaylitDownload.py -p path -u url

    args_size = len(sys.argv)
    youtube_url = ""
    path = ""

    if args_size not in [1,3,5]:
        print("Wrong number of arguments given!")
        sys.exit()
    else:
        if args_size == 1:
            youtube_url = input("Enter a youtube url: ")
        else:

            if args_size == 3:
                if sys.argv[1] == '-u':
                    youtube_url = sys.argv[2]
                else:
                    print("It's necessary inform a youtube url!")
                    sys.exit()

            else:
                if (sys.argv[1] != sys.argv[3]) and (sys.argv[1] in ['-u', '-p']) and (sys.argv[3] in ['-u', '-p']):
                    if sys.argv[1] == '-u':
                        youtube_url = sys.argv[2]
                        path = sys.argv[4]
                    else:
                        path = sys.argv[2]
                        youtube_url = sys.argv[4]
                else:
                    print("Wrong arguments given!")
                    sys.exit()

    YoutubeToMp3(youtube_url, path)



    
    
    


