#########################################
##### Name: Yilin Li                #####
#########################################
from lib2to3.pgen2.pgen import generate_grammar
from pickle import FALSE
import webbrowser
import requests
import json

class Media:

    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", json = None):
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            try:
                self.title = json["collectionName"]
            except:
                self.title = title
            try:
                self.author = json["artistName"]
            except:
                self.author = author
            try:
                self.release_year = json["releaseDate"][0:4]
            except:
                self.release_year = release_year
            try:
                self.url = json["collectionViewUrl"]
            except:
                self.url = url


    def info(self):
        return self.title + " by " + self.author + " (" + str(self.release_year) + ")" 

    def length(self):
        return 0


# Other classes, functions, etc. should go here
class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", album = "No Album", genre = "No Genre", track_length = 0, json = None):
        super().__init__(title, author, release_year, url, json = json)
        if json == None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            try:
                self.title = json["trackName"]
            except:
                self.title = title
            try:
                self.album = json["collectionName"]
            except:
                self.album = album
            try:
                self.genre = json["primaryGenreName"]
            except:
                self.genre = genre
            try:
                self.track_length = json["trackTimeMillis"]
            except:
                self.track_length = track_length

    def info(self):
        return self.title + " by " + self.author + " (" + str(self.release_year) + ")" + " [" + self.genre + "]" 
    
    def length(self):
        return round(self.track_length/1000)


class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", rating = "No Rating", movie_length = 0, json = None):
        super().__init__(title, author, release_year, url, json = json)
        if json == None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            try:
                self.title = json["trackName"]
            except:
                self.title = title
            try:
                self.rating = json["contentAdvisoryRating"]
            except:
                self.rating = rating
            try:
                self.movie_length = json["trackTimeMillis"]
            except:
                self.movie_length = movie_length

    def info(self):
        return self.title + " by " + self.author + " (" + str(self.release_year) + ")" + " [" + self.rating + "]" 

    def length(self):
        return round(self.movie_length/60000)


def json_object(term = "Beatles", limit = 50):
    BASE_URL = "https://itunes.apple.com/search"
    PARAMS = {"term":term, "limit":limit}
    r = requests.get(url = BASE_URL, params = PARAMS)
    data = r.json()["results"]

    n  = len(data)
    
    movie = []
    song = []
    media = []

    for i in range(n):
        try:
            if data[i]["kind"] == "feature-movie":
                movie.append(Movie(json = data[i]))
            elif data[i]["kind"] == "song":
                song.append(Song(json = data[i]))
            else:
                media.append(Media(json = data[i]))
        except:
            media.append(Media(json = data[i]))

    return song, movie, media


def print_list(song_list, movie_list, media_list):
    print("SONGS\n")
    count = 1
    if len(song_list) == 0:
        print("No result.\n")
    for i in range(len(song_list)):
        print(str(count) + " " + song_list[i].info() + "\n")
        count += 1
    print("MOVIES\n")
    if len(movie_list) == 0:
        print("No result.\n")
    for i in range(len(movie_list)):
        print(str(count) + " " + movie_list[i].info() + "\n")
        count += 1
    print("OTHER MEDIA\n")
    if len(media_list) == 0:
        print("No result.\n")
    for i in range(len(media_list)):
        print(str(count) + " " + media_list[i].info() + "\n")
        count += 1


def view_browser(songlist, movielist, medialist, idx):
    if idx <= len(songlist):
        print("Launching " + songlist[idx-1].url + " in web browser...")
        webbrowser.open(songlist[idx-1].url)
    elif idx <= len(songlist) + len(movielist) and idx > len(songlist):
        print("Launching " + movielist[idx-1-len(songlist)].url + " in web browser...")
        webbrowser.open(movielist[idx-1-len(songlist)].url)
    else:
        print("Launching " + medialist[idx-1-len(songlist)-len(movielist)].url + " in web browser...")
        webbrowser.open(medialist[idx-1-len(songlist)-len(movielist)].url)


def more_info(songlist, movielist, medialist, str):
    while int(str) > len(songlist) + len(movielist) + len(medialist) or int(str) <= 0:
        print("Invalid number.\n")
        str = input("Enter a number for more info, or another term, or exit: ")
        if str == "exit":
            exit()
        elif str.isnumeric():
            more_info(songlist, movielist, medialist, str)
        else:
            return
    view_browser(songlist, movielist, medialist, int(str))
    str = input("Enter a number for more info, or another search term, or exit: ")
    if str == "exit":
        exit()
    elif str.isnumeric():
        more_info(songlist, movielist, medialist, str)
    else:
        return


def main():
    str = input("Enter a search term, or \"exit\" to quit: ")
    while True:
        if str == "exit":
            exit()
        songlist, movielist, medialist = json_object(term = str)
        print_list(songlist, movielist, medialist)
        str = input("Enter a number for more info, or another term, or exit: ")
        if str == "exit":
            exit()
        elif str.isnumeric(): 
            more_info(songlist, movielist, medialist, str)
        else:
            continue
            

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    # part 3 test:
    # json_object()
    main()
