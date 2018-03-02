from lxml import html
import requests
import sys
import threading
import youtube_dl
import time

# Logger class for logging the output from youtube_dl
class Logger(object):
    def debug(self, msg):
        print "DEBUG: "+msg
    def warning(self, msg):
        print "WARN: "+msg
    def error(self, msg):
        print "ERROR: "+msg

# Callback function to prompt the completion of the download
def progress_hook(download):
    if download['status'] == 'finished':
        print 'Download Complete. Now Converting!!!'

# Options for youtube downloader
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality': '192',
    }],
    'logger':Logger(),
    'progress_hooks': [progress_hook],
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
#page = "https://gaana.com/playlist/gaana-dj-kannada-top-20"
page = "https://gaana.com/playlist/gaana-dj-gaana-international-top-50" # Links to the playlists

def getVideoLink(track_name, video_titles):
    print track_name.text
    for title in video_titles:
        try:
            if track_name.text in title.attrib['title']: # If the link has the song title in it
                base = "https://www.youtube.com"+title.attrib['href']
                ydl.download([base])
                break
        except:
            continue

# Get the html page for the song page
page = requests.get(page)
html_content_song = html.fromstring(page.content) # Get the html content in the form of a string
song_titles = html_content_song.xpath('//a[@data-type="playSong"]') # Get all the song titles

# The number of song titles
print "The number of songs: {0}".format(len(song_titles)/2)
# print "The number of artists: {0}".format(len(artist))

# print artist[0].text

for i in range(0, len(song_titles), 2):
    # Send a search query to youtube and get the
    video_page = requests.get('http://www.youtube.com/results?search_query='+"+".join(song_titles[i].text.split(" "))+"music+video") # So you only get the videos with the music
    base = video_page.content
    video_page = html.fromstring(video_page.content)
    video_titles = video_page.xpath('//a') # Just get the anchor's

    if song_titles[i].text in base:
        threading.Thread(target=getVideoLink, args=(song_titles[i], video_titles)).start() # Multi-Threading download multiple files
    else:
        print "ERROR: YouTube doesn't seem to like us....."
    time.sleep(5)
