import pandas as pd
import scrapy
from ..storage import Storage


class Colors(scrapy.Spider):
    name = "color"

    def __init__(self):
        self.s = Storage()
        self.c1, self.c2, self.c3, self.c4, self.c5 = [], [], [], [], []
        self.data = {}

    def start_requests(self):

        urls = [
            'https://www.color-hex.com/color-palettes/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_dir = 'https://www.color-hex.com'

        # extracting the style attribute to get individual colors
        palettes = response.css('div.palettecolordiv::attr(style)').extract()
        grouped_list = []

        # looping over scraped data and creating a 3d list of palettes
        for i in range(0, len(palettes), 5):
            placeholder = []
            # check for five colors and save them as one palette
            for j in range(i, i + 5):
                hex_value = self.extract_hex(palettes[j])
                rgb_list = self.convert_to_rgb(hex_value)
                placeholder.append(rgb_list)

            # add the palette to a list
            grouped_list.append(placeholder)

        try:
            next_page = response.css('.pagination li.active + li a::attr(href)').extract()[0]
            yield response.follow(base_dir + next_page, callback=self.parse)
        except:
            self.data["c1"] = pd.Series(self.c1, dtype="object")
            self.data["c2"] = pd.Series(self.c2, dtype="object")
            self.data["c3"] = pd.Series(self.c3, dtype="object")
            self.data["c4"] = pd.Series(self.c4, dtype="object")
            self.data["c5"] = pd.Series(self.c5, dtype="object")
            self.s.add_data(self.data)
            self.s.export_csv()

        # Convert data stored from 3d to 2d array
        for single_palette in grouped_list:
            # looping over palettes
            color_list = []
            for color in single_palette:
                # looping through the five colors in a palette
                for i in range(len(color)):
                    # single color string formed from rgb values
                    # convert to string
                    color[i] = str(color[i])

                # add commas between rgb values for one color in palette
                color_list.append(",".join(color))

                if (single_palette.index(color) % 5) + 1 == 1:
                    self.c1.append(color_list[-1])
                elif (single_palette.index(color) % 5) + 1 == 2:
                    self.c2.append(color_list[-1])
                elif (single_palette.index(color) % 5) + 1 == 3:
                    self.c3.append(color_list[-1])
                elif (single_palette.index(color) % 5) + 1 == 4:
                    self.c4.append(color_list[-1])
                elif (single_palette.index(color) % 5) + 1 == 5:
                    self.c5.append(color_list[-1])

    # Functions to convert values
    #####################################
    @staticmethod
    def extract_hex(html):
        # gets the hex code from html
        return html[html.index('#') + 1:]

    @staticmethod
    def convert_to_rgb(value):
        # changes the hex value to rgb and returns a list of three values
        rgb_vals = []

        if len(value) == 3:
            value = '000' + value

        for i in range(1, len(value), 2):
            try:
                rgb_vals.append(int(value[i - 1:i + 1], 16))
            except ValueError:
                rgb_vals.append('NaN')

        return rgb_vals
