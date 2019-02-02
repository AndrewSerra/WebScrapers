import scrapy

class HeadphonesSpider(scrapy.Spider):

    name = "headphones"

    def __init__(self):
        self.scraped = []

    def start_requests(self):
        urls = [
        'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=headphones&rh=i%3Aaps%2Ck%3Aheadphones&ajr=2',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        img_urls = response.css('img::attr(src)').extract()
        self.scraped.append(img_urls)
        try:
            next_page = response.css('span.pagnRA a#pagnNextLink::attr(href)').extract()[0]
            yield response.follow(next_page, callback=self.parse)
        except:
            with open('urls.txt', 'a') as f:
                for u in self.scraped:
                    f.write(str(u) + "\n")
                f.close()
