# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class LotteryPipeline:
    def __init__(self):
        self.file = open("parsed_data.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True, join_multivalued=',')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
