import scrapy,csv,time
from scraping.items import lysitem


class LysSpider(scrapy.Spider):
    ''' Class contains two property name which is the spider
        name, and Download_delay'''

    name = "lys"
    DOWNLOAD_DELAY = 0.25


    def start_requests(self):
        '''Here Fetched the catagory Squash to speed up the scraping '''

        urls = ['https://www.liveyoursport.com/squash-rackets/?page=1',
                'https://www.liveyoursport.com/squash-rackets/?page=2',
                'https://www.liveyoursport.com/squash-rackets/?page=3',
                'https://www.liveyoursport.com/squash-shoes/?page=1',
                'https://www.liveyoursport.com/squash-shoes/?page=2',
                'https://www.liveyoursport.com/squash-shoes/?page=3',
                'https://www.liveyoursport.com/squash-shoes/?page=4',
                'https://www.liveyoursport.com/squash-shoes/?page=5',
                'https://www.liveyoursport.com/squash-shoes/?page=6',
                'https://www.liveyoursport.com/Squash-strings/',
                'https://www.liveyoursport.com/squash-racket-grips/?page=1',
                'https://www.liveyoursport.com/squash-racket-grips/?page=2',
                'https://www.liveyoursport.com/squash-racket-grips/?page=3',
                'https://www.liveyoursport.com/squash-racket-grips/?page=4',
                'https://www.liveyoursport.com/squash-racket-grips/?page=5',
                'https://www.liveyoursport.com/squash-balls/',
                'https://www.liveyoursport.com/squash-racket-bags/',
                'https://www.liveyoursport.com/Squash-eye-wear/',
                'https://www.liveyoursport.com/Squash-dampners/',
                'https://www.liveyoursport.com/squash-wrist-bands/',
                'https://www.liveyoursport.com/squash-accessories/?page=1',
                'https://www.liveyoursport.com/squash-accessories/?page=2',
                'https://www.liveyoursport.com/squash-accessories/?page=3',
                'https://www.liveyoursport.com/squash-accessories/?page=4',
                'https://www.liveyoursport.com/squash-accessories/?page=5'
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        '''In here scraping all the item's page URL to scrape given attributes'''

        if(response.xpath('//*[@id="frmCompare"]/ul/li[1]/div[@class="ProductDetails"]/*').extract()):
            xp = '//*[@id="frmCompare"]/ul/li[*]/div[@class="ProductDetails"]//a//@href'
            URL     = response.xpath(xp).extract()
            for url in  URL:
                print url
                yield scrapy.Request(url=url, callback=self.parse_final)


    def parse_final(self, response):
        '''It scrape four required values from product page and yields an item'''

        item = lysitem()
        name = response.xpath('//*[@class="ProductMain"]//h1//text()').extract()
        item["name"] = name[0]
        price = response.xpath('//*[@class="ProductMain"]/div/div/div//em//text()').extract()
        item["price"] =price[0]
        description = response.xpath('//*[@id="ProductDescription"]//p[*]//text()').extract()
        description = [x.decode('utf-8') for x in description] #decoding bytes here because it has some non-ascii chars
        description = [x.encode('utf-8') for x in description]
        description = '\n'.join(description)
        item["description"] = description
        url = response.url
        item["url"] = url
        self.log('yielding Item')
        yield item

