import urllib
from bs4 import BeautifulSoup

html = urllib.request.urlopen("https://web.archive.org/web/20180803021324/https:/www.billboard.com/charts/hot-100-60th-anniversary")

soup = BeautifulSoup(html)

divs = soup.findAll("div", {"class": "chart-list-item"})[:200]

with open("billboard.txt", 'w') as f:
    for div in divs:
        rank = div["data-rank"] 
        songName = div.find("span", {"class": "chart-list-item__title-text"}).text.strip().title()
        artist = div.find("div", {"class": "chart-list-item__artist"}).text.strip()
        year = div.find("span", {"class", "chart-list-item__all-time-data-cell"}).text.strip()
        temp = div.findAll("span", {"class": "chart-list-item__all-time-data-cell"})
        year, genre, group = temp[0].text.strip(), temp[1].text.strip(), temp[2].text.strip()

        if group == 'Female':
            group = 'F'
        elif group == 'Male':
            group = 'M'
        elif group == 'Duo' or group == 'Group' or group == 'Duo/Group':
            group = 'D'

        if genre == "Latin":
            genre = 1
        elif genre == 'Country':
            genre = 2
        elif genre == "Hip-Hop/Rap":
            genre = 3
        elif genre == "Jazz":
            genre = 4
        elif genre == "Dance/Electronic":
            genre = 5
        elif genre == "R&B":
            genre = 6
        elif genre == "Pop":
            genre = 7
        elif genre == "Rock":
            genre = 8

        f.write('\n'+songName+
                '\n'+artist+
                '\n'+rank+
                '\n'+year+
                '\n'+ year[2]+'0'+
                '\n'+group+
                '\n'+str(genre))
        
        