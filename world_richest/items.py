# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorldRichestItem(scrapy.Item):
    # define the fields for your item here like:
    year:str = scrapy.Field()
    name:str = scrapy.Field()
    networth:str = scrapy.Field()
    nationality:str = scrapy.Field()

