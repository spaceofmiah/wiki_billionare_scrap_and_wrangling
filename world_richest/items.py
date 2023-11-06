# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorldRichestItem(scrapy.Item):
    # define the fields for your item here like:
    age:int = scrapy.Field()
    year:str = scrapy.Field()
    name:str = scrapy.Field()
    position:int = scrapy.Field()
    company:str = scrapy.Field()
    networth:str = scrapy.Field()


class NairaRateItem(scrapy.Item):
    buy_rate: str = scrapy.Field()
    sell_rate: str = scrapy.Field()

