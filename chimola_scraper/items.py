# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Identity


class ChimolaScraperItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    image_urls = scrapy.Field(type='list', default=list)
    category_path = scrapy.Field(type='list', default=list)


class ChimolaScraperItemLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    image_urls_out = Identity()
    category_path_out = Identity()
