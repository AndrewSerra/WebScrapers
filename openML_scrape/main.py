#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib.request
import csv
import re

link = "https://www.openml.org/search?type=data"

def write_csv_row(lst, newfile=True):
    # create csv file and enter headers
    if newfile:
        with open('datasets.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(lst)
    else:
        with open('datasets.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(lst)

# get html from the url
response = urllib.request.urlopen(link)
html = response.read().decode("utf-8")
response.close()

# find divs that contain t results
parser = BeautifulSoup(html, 'html.parser')
datasets = parser.find_all("div", {"class": "searchresult panel"})

# enter the csv headers
headers = ["name", "description", "runs", "likes", "downloads", "reach", "impact"]
write_csv_row(headers)

for dataset in datasets:
    # dataset attributes
    name = dataset.div.a.text
    description = dataset.find("div", {"class": "teaser"}).text

    b_tag_str = str(dataset.find("div", {"class": "runStats statLine"}).find("b"))

    #extracting stats from the html
    pattern = r'(?:</i>(\d+))'
    nums = re.findall(pattern, b_tag_str)
    row = [name, description] + nums
    write_csv_row(row, newfile=False)
