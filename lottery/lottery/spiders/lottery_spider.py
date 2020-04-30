import scrapy
from scrapy.http import Request
from lottery.helpers import get_dates
from lottery.items import LotteryItem
from bs4 import BeautifulSoup


class LotterySpider(scrapy.Spider):
    name = 'lottery'

    start_urls = [
        'https://lottery.com/results/us/powerball/',
    ]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def parse(self, response):

        dates = get_dates(90)  # change to 90!

        for date in dates:
            start, end = date
            modifier = f'?start={start}&end={end}'

            yield Request(
                    self.start_urls[0]+modifier,
                    headers=self.headers,
                    callback=self.parse_data
                )

    def parse_data(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'html.parser')
        base_div = soup.find('div', {'class': 'results-single-container container'})
        data_lines = base_div.find_all('a')

        for data in data_lines:
            numbers = data.find_all('div', {'class', 'lottery-ball'})
            if not numbers:
                continue

            item = LotteryItem()

            numbers_values = []
            for number in numbers:
                numbers_values.append(number.find('span').getText())

            item['results'] = numbers_values
            item['game'] = data.find('div', {'class': 'title-column'}).getText()
            item['draw_date'] = data.find('div', {'class': 'date-column'}).find('div').getText()
            item['jackpot'] = data.find('div', {'class': 'jackpot-column'}).find('span').getText()[:-7]

            yield item
