import re
from bs4 import BeautifulSoup
import scrapy
from scrapy.http.request import Request
from getters import get_urls

"""Run this command to generate the csv file :
scrapy runspider scrawler.py -o stocks.csv
"""
class MySpider(scrapy.Spider):
    name = "immoscrap"
    start_urls = get_urls()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        url = str(response.url)
        # url_part = url.split("/")

        for sub in response.xpath("(//main[@id='main-content'])[1]"):
            source = response.text

            soup = BeautifulSoup(source, 'lxml')
            s = str(soup.head.script.contents[0])
            s = s.replace('window.dataLayer = [', "")
            s = s.replace("];", "")

            s_dict = json.loads(s)
            classified = s_dict["classified"]
            print(classified)

            id = int(classified["id"])
            type_building = classified["type"]
            price = classified["price"]
            kitchen = classified["kitchen"]["type"]
            bedroom = classified["bedroom"]["count"]
            garden = classified["outdoor"]["garden"]["surface"]
            terrace = classified["outdoor"]["terrace"]["exists"]
            swimmingPool = classified["wellnessEquipment"]["hasSwimmingPool"]
            parking_indoor: classified["parkingSpaceCount"]["indoor"]
            parking_outdoor: classified["parkingSpaceCount"]["outdoor"]
            title = str(sub.xpath(
                "//div[@id='classified-description-content-text']//strong[1]/text()[last()]").get()).strip()
            surface = str(sub.xpath(
                "//th[text()[normalize-space()='Surface habitable']]/following::table/tbody[1]/tr[1]/th[1]/following-sibling::td/text()[1]").get()).strip()

            yield{

                "id": id,
                "type": type_building,
                "title": title,
                "price": price,
                "surface": surface,
                "kitchen": kitchen,
                "bedroom": bedroom,
                "garden": garden,
                "terrace": terrace,
                "swimmingPool": swimmingPool,
                "parking_indoor": parking_indoor,
                "parking_outdoor": parking_outdoor,
                "url": url
            }
