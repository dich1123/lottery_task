# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LotteryItem(scrapy.Item):
    game = scrapy.Field()
    draw_date = scrapy.Field()
    jackpot = scrapy.Field()
    results = scrapy.Field()
