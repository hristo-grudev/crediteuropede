import scrapy

from scrapy.loader import ItemLoader

from ..items import CrediteuropedeItem
from itemloaders.processors import TakeFirst


class CrediteuropedeSpider(scrapy.Spider):
	name = 'crediteuropede'
	start_urls = ['https://www.crediteurope.de/newsletter/februar-2021/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="arrow-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//nav[@class="news-side-nav"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="header-title"]/text()').get()
		description = response.xpath('//div[@class="header-description"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="breadcrumb container"]/span[3]/a/text()').get()

		item = ItemLoader(item=CrediteuropedeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
